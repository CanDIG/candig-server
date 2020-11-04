# CanDIG-Server DataBase Snapshot Report

Report generated on {{current_utc}} UTC.

## Datasets

The database contains {{number_of_datasets}} datasets

## Records

{{records}}

## Patients

{% for key, value in patient_dict.items() %}
### {{key}} dataset
```
Patients id {{value}}
```
{% endfor %}

{% if peer_list %}
## Peers

{{ peer_list }}

{% endif %}