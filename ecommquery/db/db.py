
# Redundant reference and property database


table ep;
<id>, <endpoint name>, <endpoint description>

table ep_ref_def;
<ep id>, <ref name>, <vallidation pattern>, <nullable>

# short name
# descriptive name
# EAN
# Offer ID
transaction, accurate transaction, ref, validated
updte, accurate time -

set

table ep_prop_def;
<ep id>, <prop name>, <vallidation pattern>, <nullable>

# price, stock,

# at run time
table run_ep_instances;
<ep id>, <endpoint instance name>, <creation date>. <is active>

table run_ep_item_active_ref;
<run_ep_instances id>, <ep_ref_def id>, <id>, <date>

table run_ep_associations
<run_ep_instance_active_ref id>, <value>, <date>




