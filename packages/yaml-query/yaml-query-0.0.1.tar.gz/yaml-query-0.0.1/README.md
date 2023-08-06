# yaml-query

## Usage
```
~ cat configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    app: chirper
  name: chirper
data:
  config.yaml: |
    - a
    - b
    - c
  service-config.yaml: |
    service_on: true

~ yaml-query 'metadata labels app' configmap.yaml
chirper
...

~ cat configmap.yaml | yaml-query 'data service-config.yaml'
service_on: true
...
```
