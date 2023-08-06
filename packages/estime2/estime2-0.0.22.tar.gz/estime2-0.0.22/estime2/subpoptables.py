
from estime2.config import (
    get_option,
    set_option
)
from estime2.poptable import (
    PopTable,
    return_goption_if_None
)
from estime2.poptable_resultswrapper import PopTableResultsWrapper
from typing import Collection as Axes
from typing import (
    List,
    Optional,
    Union
)
import numpy as np
import warnings

# pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')
Dtype = Union[str, np.dtype, "ExtensionDtype"]



class ProvPopTable(PopTable):
    '''
    A table of populations and components at a provincial level.
    '''
    
    def __init__(
        self,
        data = None,
        index: Optional[Axes] = None,
        columns: Optional[Axes] = None,
        dtype: Optional[Dtype] = None,
        copy: bool = False,
        pop_sex: Optional[str] = None,
        pop_age: Optional[str] = None,
        pop_end: Optional[str] = None,
        pop_start: Optional[str] = None,
        pop_birth: Optional[str] = None,
        comp_neg_temp_out: Optional[str] = None,
        comp_neg_emi: Optional[str] = None,
        comp_neg_npr_out: Optional[str] = None,
        comp_neg_death: Optional[str] = None,
        comp_neg_interprov_out: Optional[str] = None,
        comp_neg_intraprov_out: Optional[str] = None,
        comp_neg_etc: Optional[List[str]] = None,
        comp_neg_put_etc_before: Optional[bool] = None,
        comp_pos_temp_in: Optional[str] = None,
        comp_pos_ret_emi: Optional[str] = None,
        comp_pos_npr_in: Optional[str] = None,
        comp_pos_immi: Optional[str] = None,
        comp_pos_interprov_in: Optional[str] = None,
        comp_pos_intraprov_in: Optional[str] = None,
        comp_pos_etc: Optional[List[str]] = None,
        comp_pos_put_etc_before: Optional[bool] = None,
        comp_end: Optional[List[str]] = None,
        reorder_cols: bool = True,
        show_pop_end: bool = False,
        is_subprov: bool = False,
        flag: bool = True
    ):

        # is_subprov must be False all the time
        # flag may be False if data is already grouped and summed by
        # pop.sex and pop.age
        if is_subprov:
            raise ValueError(
                "When creating an instance of ProvPopTable, "
                f"`is_subprov` must be False, and not {is_subprov}."
            )
        super().__init__(
            data, index, columns, dtype, copy,
            pop_sex,
            pop_age,
            pop_end,
            pop_start,
            pop_birth,
            comp_neg_temp_out,
            comp_neg_emi,
            comp_neg_npr_out,
            comp_neg_death,
            comp_neg_interprov_out,
            comp_neg_intraprov_out,
            comp_neg_etc,
            comp_neg_put_etc_before,
            comp_pos_temp_in,
            comp_pos_ret_emi,
            comp_pos_npr_in,
            comp_pos_immi,
            comp_pos_interprov_in,
            comp_pos_intraprov_in,
            comp_pos_etc,
            comp_pos_put_etc_before,
            comp_end,
            reorder_cols,
            show_pop_end,
            is_subprov,
            flag
        )

    def fix_issues(
        self, 
        method: Optional[str] = None, 
        return_all_mods: bool = False
    ):
        '''
        Apply modifications and counter-adjustments to `self` so that there
        are no negative end-of-period population. Figures for counter-
        adjustments in neighbouring ages are different based on `method`
        specified. Set `return_all_mods` to `True` to get all the 
        modifications and counter-adjustments made to `self`.

        Usage
        -----
        `ProvPopTable.fix_issues(
            method: Optional[str] = None, 
            return_all_mods: bool = False
        )`

        Argument
        --------
        * `method`: the same argument as in `self.get_K(comp, method, J)`.
        * `return_all_mods`: a bool (`False` by default); if `True`, this 
            will return all the modifications and counter-adjustments made
            to `self`.

        Details
        -------
        For each problematic record, it modifies problematic record(s) and
        makes counter-adjustments to records of neighbouring ages within a 
        component according to the `method` specified. For each component, 
        the modification and counter-adjustments made to that component of 
        `self` will affect the end-of-period population. The process is 
        done until no new end-of-period population is negative.
        In case of `return_all_mods` is `True`, this method records how
        much of modification and counter-adjustments are made, and returns
        a `PopTableResultsWrapper` object.

        Returns
        -------
        If `return_all_mods` is `False`, then it returns a fixed version
        of `self`, the current `ProvPopTable`. 
        If `return_all_mods` is `True`, then regardless of whether or not
        there are corrections made to the original table, it returns a 
        `PopTableResultsWrapper`.
        '''

        args_in_self = self.get_args()
        prevs = {}
        for k, v in args_in_self.items():
            prevs[k] = get_option(k)
            set_option(k, v)

        comp_neg_to_use = self.get_comp_neg()
        comp_pos_to_use = self.get_comp_pos()
        comps = comp_neg_to_use + comp_pos_to_use

        pop_groups = self.get_pop_groups()
        pop_sex = pop_groups[0]
        all_cols = self.columns.tolist()
        show_pop_end = self.get_pop_end() in all_cols
        comps_modified = []
        sexes = np.unique(self[pop_sex])
        self_copy = None
        method = return_goption_if_None('method', method)

        for sex in sexes:
            self_cp_sex =\
                self.copy().loc[lambda df: df[pop_sex] == sex]
            self_cp_sex = ProvPopTable(
                self_cp_sex,
                reorder_cols = False, # since it is reordered already
                show_pop_end = show_pop_end,
                # flag = False since it is grouped and summed already
                flag = False
            )
            # `flag` is True iff `I` has at least one nonzero value
            flag = (sum(self_cp_sex.get_I()['I'].values != 0) != 0)
            i = 0
            num_zeros = sum(self_cp_sex.get_I()['I'].values == 0)
            while flag:
                comp = comps[i]
                self_cp_sex = apply_L(
                    self_cp_sex, 
                    comp, 
                    method,
                    comps_modified
                )
                I_vec = self_cp_sex.get_I()['I'].values
                new_num_zeros = sum(I_vec == 0)
                if all(I_vec == 0):
                    # all problematic records fixed
                    flag = False # stop the while-loop iteration
                elif num_zeros != new_num_zeros:
                    # one problematic record fixed
                    i = 0 # move to the next problematic record
                    num_zeros = new_num_zeros # assign a new number
                elif i != (len(comps) - 1): 
                    # correction in progress
                    i += 1
                else: 
                    # i.e. lack of values for corrections
                    # Correction could not be made to the problematic 
                    # record at the youngest age.
                    # If the youngest problematic record cannot be fixed, 
                    # then any older problematic records cannot be fixed 
                    # either.
                    # intraprov_in or intraprov_out should be modified 
                    # in SubProvPopTable
                    flag = False

            if self_copy is None:
                self_copy = self_cp_sex
            else:
                self_copy = self_copy\
                    .append(self_cp_sex, ignore_index = True)

        self_copy = ProvPopTable(
            self_copy.sort_values(pop_groups),
            reorder_cols = False, # since it is reordered already
            show_pop_end = show_pop_end,
            # flag = False since it is grouped and summed already
            flag = False
        )

        for k2, v2 in prevs.items():
            set_option(k2, v2)

        if return_all_mods:
            if method == '1dist':
                musp = get_option("method_use.second_pass")
                museq = get_option("method_use.seq")
                aps = get_option("age.prop_size")
                pass2 = ", 2nd pass" if musp else ""
                pass2seq =\
                    f", {aps}-year sequence" if (musp and museq) else ""
                method = f"{method}{pass2}{pass2seq}"
            result = PopTableResultsWrapper(
                orig_table = self, 
                result_fix_issues = [self_copy] + comps_modified,
                method = method
            )
            return result
        else:
            return self_copy

class SubProvPopTable(PopTable):
    '''
    A table of populations and components at a subprovincial level.
    '''

    def __init__(
        self,
        data = None,
        index: Optional[Axes] = None,
        columns: Optional[Axes] = None,
        dtype: Optional[Dtype] = None,
        copy: bool = False,
        pop_sex: Optional[str] = None,
        pop_age: Optional[str] = None,
        pop_end: Optional[str] = None,
        pop_start: Optional[str] = None,
        pop_birth: Optional[str] = None,
        comp_neg_temp_out: Optional[str] = None,
        comp_neg_emi: Optional[str] = None,
        comp_neg_npr_out: Optional[str] = None,
        comp_neg_death: Optional[str] = None,
        comp_neg_interprov_out: Optional[str] = None,
        comp_neg_intraprov_out: Optional[str] = None,
        comp_neg_etc: Optional[List[str]] = None,
        comp_neg_put_etc_before: Optional[bool] = None,
        comp_pos_temp_in: Optional[str] = None,
        comp_pos_ret_emi: Optional[str] = None,
        comp_pos_npr_in: Optional[str] = None,
        comp_pos_immi: Optional[str] = None,
        comp_pos_interprov_in: Optional[str] = None,
        comp_pos_intraprov_in: Optional[str] = None,
        comp_pos_etc: Optional[List[str]] = None,
        comp_pos_put_etc_before: Optional[bool] = None,
        comp_end: Optional[List[str]] = None,
        reorder_cols: bool = True,
        show_pop_end: bool = False,
        is_subprov: bool = True,
        flag: bool = True
    ):
        '''
        Create an instance of SubProvPopTable. Note that every cell of the
        table except for those in the end-of-period population column
        should have non-negative values.

        Usage
        -----
        SubProvPopTable(
            data = None,
            index: Optional[Axes] = None,
            columns: Optional[Axes] = None,
            dtype: Optional[Dtype] = None,
            copy: bool = False,
            pop_sex: Optional[str] = None,
            pop_age: Optional[str] = None,
            pop_end: Optional[str] = None,
            pop_start: Optional[str] = None,
            pop_birth: Optional[str] = None,
            comp_neg_temp_out: Optional[str] = None,
            comp_neg_emi: Optional[str] = None,
            comp_neg_npr_out: Optional[str] = None,
            comp_neg_death: Optional[str] = None,
            comp_neg_interprov_out: Optional[str] = None,
            comp_neg_intraprov_out: Optional[str] = None,
            comp_neg_etc: Optional[List[str]] = None,
            comp_neg_put_etc_before: Optional[bool] = None,
            comp_pos_temp_in: Optional[str] = None,
            comp_pos_ret_emi: Optional[str] = None,
            comp_pos_npr_in: Optional[str] = None,
            comp_pos_immi: Optional[str] = None,
            comp_pos_interprov_in: Optional[str] = None,
            comp_pos_intraprov_in: Optional[str] = None,
            comp_pos_etc: Optional[List[str]] = None,
            comp_pos_put_etc_before: Optional[bool] = None,
            comp_end: Optional[List[str]] = None,
            reorder_cols: bool = True,
            show_pop_end: bool = False
        )

        Arguments
        ---------
        * `data`, `index`, `columns`, `dtype`, `copy`: inherited from 
            `pandas.DataFrame`
        * `pop_sex`, `pop_age`, `pop_end`, `pop_start`, `pop_birth`, 
            `comp_neg_temp_out`, `comp_neg_emi`, `comp_neg_npr_out`,
            `comp_neg_death`, `comp_neg_interprov_out`, 
            `comp_neg_intraprov_out`, `comp_neg_etc`,
            `comp_pos_temp_in`, `comp_pos_ret_emi`, `comp_pos_npr_in`,
            `comp_pos_immi`, `comp_pos_interprov_in`, 
            `comp_pos_intraprov_in`, `comp_pos_etc`,
            `comp_end`, `reorder_cols`, `show_pop_end`: inherited from
            `ProvPopTable`
        * `comp_neg_put_etc_before`: (`None` by default) a bool; if `True`,
            then components in `comp_neg.etc` will precede 
            `comp_neg.interprov_out` and `comp_neg.intraprov_out`, and 
            follow other conventional negative components. If `False`, 
            components will follow `comp_neg.intraprov_out` instead. 
            If `None`, then it uses a global option value 
            `estime2.options.comp_neg.put_etc_before` (`False` by default).
        * `comp_pos_put_etc_before`: (`None` by default) a bool; if `True`,
            then components in `comp_pos.etc` will precede 
            `comp_pos.interprov_in` and `comp_pos.intraprov_in`, and follow
            other conventional positive components. If `False`, components
            will follow `comp_pos.intraprov_in` instead. If `None`, then it
            uses a global option value 
            `estime2.options.comp_pos.put_etc_before` (`False` by default).
        
        Details
        -------
        1. `SubProvPopTable` is a special case of `ProvPopTable` where
            `is_subprov` is `True`.
        2. If `reorder_cols` is `True`, then the columns of `data` is
            reordered in the following order from the left. For a column
            corresponding to one of the `comp_*` arguments, it will be
            displayed in the table iff neither the argument nor the 
            corresponding global option is `None` or `[]`: 
                + `pop_sex`
                + `pop_age`
                + `pop_end` (if `show_pop_end` is True)
                + `pop_start`
                + `pop_birth`
                + `comp_neg_temp_out` 
                + `comp_neg_emi`
                + `comp_neg_npr_out`
                + `comp_neg_death`
                + `comp_neg_etc` (if given any & put_etc_before is True)
                + `comp_neg_interprov_out`
                + `comp_neg_intraprov_out`
                + `comp_neg_etc` (if given any & put_etc_before is False)
                + `comp_pos_temp_in`
                + `comp_pos_ret_emi`
                + `comp_pos_npr_in`
                + `comp_pos_immi`
                + `comp_pos_etc` (if given any & put_etc_before is True)
                + `comp_pos_interprov_in`
                + `comp_pos_intraprov_in`
                + `comp_pos_etc` (if given any & put_etc_before is False)
        3. Whether or not `reorder_cols` is `True`, the method looks for
            the component(s) responsible for the negative end-of-period
            population following the above order of `comp_*`'s.
        '''

        # is_subprov must be True all the time
        # flag may be False if data is already grouped and summed by
        # pop.sex and pop.age
        if not is_subprov:
            raise ValueError(
                "When creating an instance of SubProvPopTable, "
                f"`is_subprov` must be True, and not {is_subprov}."
            )
        super().__init__(
            data, index, columns, dtype, copy,
            pop_sex,
            pop_age,
            pop_end,
            pop_start,
            pop_birth,
            comp_neg_temp_out,
            comp_neg_emi,
            comp_neg_npr_out,
            comp_neg_death,
            comp_neg_interprov_out,
            comp_neg_intraprov_out,
            comp_neg_etc,
            comp_neg_put_etc_before,
            comp_pos_temp_in,
            comp_pos_ret_emi,
            comp_pos_npr_in,
            comp_pos_immi,
            comp_pos_interprov_in,
            comp_pos_intraprov_in,
            comp_pos_etc,
            comp_pos_put_etc_before,
            comp_end,
            reorder_cols,
            show_pop_end,
            is_subprov,
            flag
        )

    def fix_issues(
        self, 
        method: Optional[str] = None, 
        return_all_mods: bool = False
    ):
        '''
        Apply modifications and counter-adjustments to `self` so that there
        are no negative end-of-period population. Figures for counter-
        adjustments in neighbouring ages are different based on `method`
        specified. Set `return_all_mods` to `True` to get all the 
        modifications and counter-adjustments made to `self`.

        Usage
        -----
        `SubProvPopTable.fix_issues(
            method: Optional[str] = None, 
            return_all_mods: bool = False
        )`

        Argument
        --------
        * `method`: the same argument as in `self.get_K(comp, method, J)`.
        * `return_all_mods`: a bool (`False` by default); if `True`, this 
            will return all the modifications and counter-adjustments made
            to `self`.

        Details
        -------
        For each problematic record, it modifies problematic record(s) and
        makes counter-adjustments to records of neighbouring ages within a 
        component according to the `method` specified. For each component, 
        the modification and counter-adjustments made to that component of 
        `self` will affect the end-of-period population. The process is 
        done until no new end-of-period population is negative.
        In case of `return_all_mods` is `True`, this method records how
        much of modification and counter-adjustments are made, and returns
        a `PopTableResultsWrapper` object.

        Returns
        -------
        If `return_all_mods` is `False`, then it returns a fixed version
        of `self`, the current `SubProvPopTable`. 
        If `return_all_mods` is `True`, then regardless of whether or not
        there are corrections made to the original table, it returns a 
        `PopTableResultsWrapper`.
        '''

        args_in_self = self.get_args()
        prevs = {}
        for k, v in args_in_self.items():
            prevs[k] = get_option(k)
            set_option(k, v)

        comp_neg_to_use = self.get_comp_neg()
        comp_pos_to_use = self.get_comp_pos()
        comps = comp_neg_to_use + comp_pos_to_use

        pop_groups = self.get_pop_groups()
        pop_sex = pop_groups[0]
        all_cols = self.columns.tolist()
        show_pop_end = self.get_pop_end() in all_cols
        comps_modified = []
        sexes = np.unique(self[pop_sex])
        self_copy = None
        method = return_goption_if_None('method', method)

        for sex in sexes:
            self_cp_sex =\
                self.copy().loc[lambda df: df[pop_sex] == sex]
            self_cp_sex = SubProvPopTable(
                self_cp_sex,
                reorder_cols = False, # since it is reordered already
                show_pop_end = show_pop_end,
                # flag = False since it is grouped and summed already
                flag = False
            )
            # `flag` is True iff `I` has at least one nonzero value
            flag = (sum(self_cp_sex.get_I()['I'].values != 0) != 0)
            i = 0
            num_zeros = sum(self_cp_sex.get_I()['I'].values == 0)
            while flag:
                comp = comps[i]
                self_cp_sex = apply_L(
                    self_cp_sex, 
                    comp, 
                    method,
                    comps_modified
                )
                I_vec = self_cp_sex.get_I()['I'].values
                new_num_zeros = sum(I_vec == 0)
                if all(I_vec == 0):
                    # all problematic records fixed
                    flag = False # stop the while-loop iteration
                elif num_zeros != new_num_zeros:
                    # one problematic record fixed
                    i = 0 # move to the next problematic record
                    num_zeros = new_num_zeros # assign a new number
                elif i != (len(comps) - 1): 
                    # correction in progress
                    i += 1
                else: 
                    # i.e. lack of values for corrections
                    # Correction could not be made to the problematic 
                    # record at the youngest age.
                    # If the youngest problematic record cannot be fixed, 
                    # then any older problematic records cannot be fixed 
                    # either.
                    # intraprov_in or intraprov_out should be modified 
                    # in SubProvPopTable
                    flag = False

            if self_copy is None:
                self_copy = self_cp_sex
            else:
                self_copy = self_copy\
                    .append(self_cp_sex, ignore_index = True)

        self_copy = SubProvPopTable(
            self_copy.sort_values(pop_groups),
            reorder_cols = False, # since it is reordered already
            show_pop_end = show_pop_end,
            # flag = False since it is grouped and summed already
            flag = False
        )

        for k2, v2 in prevs.items():
            set_option(k2, v2)

        if return_all_mods:
            if method == '1dist':
                musp = get_option("method_use.second_pass")
                museq = get_option("method_use.seq")
                aps = get_option("age.prop_size")
                pass2 = ", 2nd pass" if musp else ""
                pass2seq =\
                    f", {aps}-year sequence" if (musp and museq) else ""
                method = f"{method}{pass2}{pass2seq}"
            result = PopTableResultsWrapper(
                orig_table = self, 
                result_fix_issues = [self_copy] + comps_modified,
                method = method
            )
            return result
        else:
            return self_copy

def apply_L(
    poptbl: Union[ProvPopTable, SubProvPopTable], 
    comp: str, 
    method: str, 
    comps_modified: List
):
    '''
    Add the return value of `poptbl.get_L(comp, method)` to the `comp`
    component of `poptbl`. Also, mutate `comps_modified` so that whenever
    the correction is applied (i.e. "L" is added) to `poptbl`, 
    `comps_modified` is appended with that correction "L".
    
    Usage
    -----
    `apply_L(
        poptbl: Union[ProvPopTable, SubProvPopTable], 
        comp: str, 
        method: str, 
        comps_modified: List
    )`

    Arguments
    ---------
    * `poptbl`: a `PopTable` with an unique sex. That is, only one sex
        exists in the table.
    * `comp`, `method`: `str`s; arguments for `poptbl.get_L(comp, method)`
    * `comps_modified`: a `list`; a list of `poptbl.get_L(comp, method)`
        whose "`comp`_L" column contains at least one nonzero value.
    '''

    pop_groups = poptbl.get_pop_groups()
    pop_age = pop_groups[1]
    all_cols = poptbl.columns.tolist()
    show_pop_end = poptbl.get_pop_end() in all_cols
    is_subprov = poptbl.is_subprov()

    comp_L = f"{comp}_L"
    L = poptbl.get_L(comp, method)
    if any(L[comp_L].values != 0):
        comps_modified.append([L, 'L', 'itself'])
    L[pop_age] = L[pop_age].apply(str)

    poptbl_cp = poptbl.copy()
    poptbl_cp[pop_age] = poptbl_cp[pop_age].apply(str)
    poptbl_cp = poptbl_cp.merge(L, on = pop_groups, how = "left")
    poptbl_cp.fillna(0, inplace = True)
    poptbl_cp[comp_L] = poptbl_cp[comp_L].apply(int)
    poptbl_cp[comp] += poptbl_cp[comp_L]
    del poptbl_cp[comp_L]

    if is_subprov:
        poptbl_cp = SubProvPopTable(
            poptbl_cp,
            reorder_cols = False, # since it is reordered already
            show_pop_end = show_pop_end,
            # flag = False since it is grouped and summed already
            flag = False     
        )
    else:
        poptbl_cp = ProvPopTable(
            poptbl_cp,
            reorder_cols = False, # since it is reordered already
            show_pop_end = show_pop_end,
            # flag = False since it is grouped and summed already
            flag = False          
        )

    return poptbl_cp
