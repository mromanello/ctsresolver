# CTS Resolver: resolvable URIs for CTS URNs

## in a nutshell

No more than a first stab at implementing a CTS resolver as Django Python application. The resolver should allow the community to register existing CTS repositories and aims to provide resolvable and de-referenciable CTS URNs for use in Semantic Web and/or Linked Open Data applications.

## ideas for the implementation

The resolver should work as follows:

* accept as `input` a list of available CTS repositories
* for each repository in the repository list
	* sanity check: check if the repository answers in a reasonable time to the basic CTS requests
	* harvest the catalog to know which which texts are available
		* store and index the CTS URNs for easy/fast retrieval

The directory `resolv` shall contain the classes needed to store persistent objects into Django.

The file `CTS.py` contains an initial implementation of some basic CTS-related classes (e.g. CTS URN, TextGroup, TextInventory, etc.).

