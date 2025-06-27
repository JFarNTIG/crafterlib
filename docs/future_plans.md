## Current known issues

### For each item, ItemGraph can only have one recipe.

Say multiple recipes are added for the same item, for example:
* 9x Gold Nugget -> 1x Gold Ingot
* 1x Raw Iron, 1/8x Coal -> 1x Gold Ingot

Currently, ItemGraph accepts the first recipe, but discards the second. In crafting
calculations, only one possible recipe is considered. This is a limitation of how
items and recipes are currently represented as networkx graphs.

However, it should be possible to encode some additional information in the graph
so that the one item graph can represent multiple recipes. This might require
rewriting large portions of code, though, and potentially break some things.

Strategy: Maybe we can add a `recipe_hash` weight to edges in the item graph.
To get different recipes for a certain item, we can thus look at the entire set of edges,
and sort the edges into buckets depending on hash. Each bucket then represents a unique
recipe for the item.