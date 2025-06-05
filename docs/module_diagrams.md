# Module Relationships

```mermaid
graph TD;
    subgraph Core
        analytics --> utils
        data --> config_utils
        generate_report --> data
        management --> generate_report
    end
    scripts --> management
    scripts --> generate_report
```

The diagram highlights the high level dependencies between major packages.
