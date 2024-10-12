import gurobipy as gp
import numpy as np

"""------------Utils for gurobipy v10---------------------

A temporary solution for modify & access *Mvar-based* models using external functions.
NOTE: Serval functions may be replaced when new version of gurobi is released.

=================       ================================     ======================================
Fun. Name                            Usage                                Dependent Fun.
=================       ================================     ======================================
_getMvarByName          Mvar version of getVarByName                     NA

_getX_MvarByName        Mvar version of Var.X                   _getMvarByName

_fixMvar                refer to JuMP.fix(var, para)            _getMvarByName, _removeMvarConstrs

_removeMvarConstrs      refer to JuMP.delete(model, con)        _getMvarByName

=================       ================================     ======================================

"""

def _getMvarByName(
    model:gp.Model,
    mvar_name:str,
    shape:list
) -> dict:
    """
    Mar version of getVarByName

    Args:
        model (gp.Model): gurobi model
        mvar_name (str): mvar name defined in gurobi model
        dim (list): dimension of mvar. For 1D mvar, dim = [i]. For 2D mvar, dim = [i,j]

    Returns:
        dict: a dictionary of mvar, which links the original mvar name to a new name that can be used in external functions
    """
    mvars_ = {}
    if len(shape) == 1:
        for i in range(shape[0]):
            mvars_[i] = model.getVarByName(mvar_name + "[%d]" % (i))    
                 
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                mvars_[i,j] = model.getVarByName(mvar_name + "[%d,%d]" % (i,j))  
                      
    else:
        raise ValueError("Currently only 1D and 2D mvars are supported")
        
    return mvars_

def _getX_MvarByName(
    model:gp.Model,
    mvar_name:str,
    shape:list
) -> np.ndarray:
    """
    Mvar version of Var.X. Currently only support 1D and 2D mvars.

    Args:
        model (gp.Model): gurobi model
        mvar_name (str): mvar name defined in gurobi model
        shape (list): dimension of mvar. For 1D mvar, dim = [i]. For 2D mvar, dim = [i,j]

    Returns:
        np.ndarray: value of mvar
    """
    
    dic = _getMvarByName(model, mvar_name, shape)
    res_X = np.zeros(shape)
    if len(shape) == 1:
        for i, value in dic.items():
            res_X[i] = value.X
    
    elif len(shape) == 2:
        for (i,j), value in dic.items():
            res_X[i,j] = value.X
    
    else:
        raise ValueError("Currently only 1D and 2D mvars are supported")
    
    return res_X

def _fixMvar(
    model:gp.Model, 
    mvar_name:str, 
    shape:list, 
    value:np.ndarray, 
    cons_name:str
) -> None:
    """
    Mvar version of JuMP.fix(var, para)

    Args:
        model (gp.Model): gurobi model
        mvar_name (str): mvar name defined in gurobi model
        shape (list): dimension of mvar. For 1D mvar, dim = [i]. For 2D mvar, dim = [i,j]
        value (np.ndarray): fixed value
        cons_name (str): name of the constraint for var fixing
    """
    dict_mvar = _getMvarByName(model, mvar_name, shape)
    if value.ndim == 1:
        # check if the var-fixing constraint already exists
        if model.getConstrByName(cons_name + "[0]") is not None:
            _removeMvarConstrs(model, cons_name, shape)
            
        model.addConstrs((dict_mvar[i] == value[i] for i in range(len(value))), name=cons_name)
        
    elif value.ndim == 2:
        if model.getConstrByName(cons_name + "[0,0]") is not None:
            _removeMvarConstrs(model, cons_name, shape)
            
        model.addConstrs((dict_mvar[i,j] == value[i,j] for i in range(value.shape[0]) for j in range(value.shape[1])), name=cons_name)
        
    else:
        raise ValueError("Currently only 1D and 2D mvars are supported")
    
    model.update()
    
def _removeMvarConstrs(
    model:gp.Model,
    cons_name:str, 
    shape:list
) -> None:
    """
    Mvar version of JuMP.delete(model, con)

    Args:
        model (gp.Model): gurobi model
        cons_name (str): name of the constraint for var fixing
        shape (list): dimension of mvar. For 1D mvar, dim = [i]. For 2D mvar, dim = [i,j]
    """
    # Get constraints to be removed
    cons = {}
    if len(shape) == 1:
        for i in range(shape[0]):
            cons[i] = model.getConstrByName(cons_name + "[%d]" %(i))
            
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                cons[i, j] = model.getConstrByName(cons_name + "[%d,%d]" %(i, j))
    else:
        raise ValueError("Currently only 1D and 2D mvars are supported")
                
    model.remove(cons) # remove constraints
    model.update()