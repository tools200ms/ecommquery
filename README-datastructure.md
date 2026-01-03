# MISOt DB

Minimalist inter-sected object database (with time and event logging)

Multi-parameter multi-data source database structure with event logging


## Concept

This database structure has been developed to handle objects that has: 

- multiple parameters
- parameters are set using multiple various sources

database also does: 

- trace the source of all parameters
- keeps change history
- annotates what caused a certain action


This is to handle scenario that happen in [ecommquery](https://github.com/tools200ms/ecommquery) framework. The framework has been developed for intenet marchants In this case, the object is a product that is on intentet sale. Each product has multiple parameters, such as, name, EAN code, price, stock, weight etc..

One product can be sold on multiple platforms, hence multiple parameters are feed by multiple sources: auction sites, internet stores.

Each parameter is annotated to trace back what was the source for a given value (in this case what internet store). Moreover, we need to call certain actions upon a certain changes (such as stock change). Hance this database structure keeps track of what method (eg. Python method) has been invokd to process given update.

This database structure is generic, therefore can be applied to another cases. 

- multiple object parameters
- multiple data sources
- need to trace changes
- need to annotate what actions has been called

Belo, deails about structre are presented: 

## Structure

At the top there is a `space`, the space is divided into portions - such as disk.

There might be mulitple speces defined, and multiple partitions within space. There is no sub-partitions, nor sub-spaces.

There is a property set defined, property can be global, or bound to a certain space.

All data updates are preceded by `object checkout`. `Object checkout` has its source, that is defined in `Object checkout sources` and has a scope limited to a given partition. Also, it provides reference toPython mehod invoked.

First, `Object chackuot` is called - that comes always with call of a spectifi Python mehod. After, a certain properties can be updated - if a new value is found.

Object is composed of parameters, parameters can be global, or space bound.

**The key concept is a fact that object can belong to multiple partions, or in other words. be characterised by having properties from diffrent spaces.**

Importantl, nothing is removed, all changes are annotated - thus it is posigble to trace what made a given change.

# Summary


This database stucture was designed to make it as simmple as possible, but still to provide comprehensive data handling. The structure is below 10 tables.


