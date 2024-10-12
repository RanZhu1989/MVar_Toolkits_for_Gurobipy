# MVar Toolkits for Gurobipy v10+

## 1. Introduction
The latest version of Gurobi (v10.0) introduced the matrix variable (Mvar) type. It is a very useful tool for modeling. However, it is not easy to access the Mvar like getVarByName() from a outside function. Especially for the case that we want to fix the Mvar in the outside of the model. Moreover, we can hardly get the value of the Mvar by using the getAttr() function. This toolkits is developed to access the Mvar in the outside of the model, which is inspired by the [JuMP](https://github.com/jump-dev/JuMP.jl) functions.
> NOTE: Serval functions may be replaced when new version of gurobi is released.

## 2. Functions
A temporary solution for fix & access *Mvar-based* models using external functions.
|MVar version (This toolkits) | Usage | Var version (Official) | 
|---|---|---|
| _getMvarByName | Mvar version of getVarByName   | NA   | 
|_getX_MvarByName| Mvar version of Var.X     |  _getMvarByName | 
| _fixMvar      | refer to JuMP.fix(var, paras)    |  _getMvarByName, _removeMvarConstrs | 
| _removeMvarConstrs  | refer to JuMP.delete(model, cons)    |  _getMvarByName | 

## 3. Imitation
Currently only support 1D and 2D mvars.

## 4. Tutorial
Import the toolkits by using the following code:
```python
from MVarToolkits import _fixMvar, _getX_MvarByName
```
Please refer to Tools.ipynb for more details.
## 5. Application
This toolkits is used for updating the optimzation model-based reinforcement learning environment in the [repository](https://github.com/RanZhu1989/IL_Self_Healing).