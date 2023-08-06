# Copyright 2018 Catalyst IT Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


def _build_subfields_query(subfields):
    root_fields = []
    subfield_payload = {}
    for subfield in subfields.items():
        root_fields.append(subfield[0])
        keys, value = _build_subfield_query({subfield[0]: subfield[1]})
        keys = [f"[{k}]" for k in keys]
        subfield_payload[f"fields{''.join(keys)}"] = value
    return root_fields, subfield_payload


def _build_subfield_query(subfield):
    if isinstance(subfield, dict):
        keys = list(subfield.keys())
        if len(keys) != 1:
            raise TypeError("Incorrectly formatted subfield query dict.")
        recursive_val = _build_subfield_query(subfield[keys[0]])
        if isinstance(recursive_val, tuple):
            keys += recursive_val[0]
            recursive_val = recursive_val[1]
        return keys, recursive_val
    elif isinstance(subfield, (list, set, tuple)):
        return ",".join(subfield)
    elif isinstance(subfield, (str)):
        return subfield

    raise TypeError(f"Unsupported type in subfield query: '{type(subfield)}'")


def build_fields_query(fields):
    """Build the fields variable into the structure RT expects

    RT expects:
    {"field": "FieldA,FieldB,FieldC...",
     "field[FieldA]": "Subfield1...",
     "field[FieldA][Subfield1]": "Sub-subfield..."}

    But because we really shouldn't be working with those kinds
    of keys directly, we allow passing in field queries as lists and
    nested dicts, that we then parse into that formatself.

    Example input:
        - 'FieldA'
        - ['FieldA', 'FieldB', 'FieldC']
        - {'FieldA': {'SubfieldA': 'Sub-subfieldA'}}
        - ["FieldA", "FieldB", {"FieldC": {"SubfieldC": "Sub-subfieldC"}}]
        - {'FieldA': {'SubfieldA': {'Sub-subfieldA': 'Sub-sub-subfieldA'}}}
        - ['FieldA', 'FieldB', {'FieldC': {'SubfieldC': 'Sub-subfieldC'}}]
    """
    payload = {}

    if isinstance(fields, dict):
        root_fields, subfield_payload = _build_subfields_query(fields)
        # NOTE(adriant): For testing and consistency, we want the fields
        #                sorted, but a set breaks that, so we do this.
        unique_non_sub_fields = sorted(list(set(root_fields)))
        payload["fields"] = ",".join(unique_non_sub_fields)
        payload.update(subfield_payload)
    elif isinstance(fields, (list, set, tuple)):
        non_sub_fields = []
        for f in fields:
            if isinstance(f, dict):
                root_fields, subfield_payload = _build_subfields_query(f)
                non_sub_fields += root_fields
                payload.update(subfield_payload)
            elif isinstance(f, (list, set, tuple)):
                non_sub_fields += list(f)
            else:
                non_sub_fields.append(f)
        # NOTE(adriant): For testing and consistency, we want the fields
        #                sorted, but a set breaks that, so we do this.
        unique_non_sub_fields = sorted(list(set(non_sub_fields)))
        payload["fields"] = ",".join(unique_non_sub_fields)
    else:
        payload["fields"] = fields

    return payload
