{% macro synapse__get_test_sql(main_sql, fail_calc, warn_if, error_if, limit) -%}
  {% set target_schema = var('synapse_test_schema', generate_schema_name() ) %}

  {# Check if the main_sql contains a WITH statement #}
  {% set with_statement = 'with\s+(\w+)\s+as' -%}
  {% set re = modules.re %}
  {% set is_match = re.match(with_statement, main_sql, re.IGNORECASE) -%}

  {% if is_match -%}

    {% set temp_table_name -%}
      #dbttesttmp_{{ range(1300, 19000) | random }}
    {% endset -%}

    {# Escape single quotes #}
    {% set sql = main_sql.replace("'", "''") -%}

    {# Check temp table existence before dropping #}
    EXEC('if object_id(n''tempdb..{{ temp_table_name }}'') is not null drop table {{ temp_table_name }};')

    EXEC('create table {{ temp_table_name }}
    with
    ( distribution = round_robin
      , heap )
    as
    {{ sql }};')

    select
      {{ "top (" ~ limit ~ ')' if limit != none }}
      {{ fail_calc }} as failures,
      case when {{ fail_calc }} {{ warn_if }}
        then 'true' else 'false' end as should_warn,
      case when {{ fail_calc }} {{ error_if }}
        then 'true' else 'false' end as should_error
    from (
      select * from {{ temp_table_name }}
    ) dbt_internal_test;

    EXEC('drop table {{ temp_table_name }};')

  {% else -%}

    {# No CTE so proceed with statement as a subquery #}
    select
      {{ "top (" ~ limit ~ ')' if limit != none }}
      {{ fail_calc }} as failures,
      case when {{ fail_calc }} {{ warn_if }}
        then 'true' else 'false' end as should_warn,
      case when {{ fail_calc }} {{ error_if }}
        then 'true' else 'false' end as should_error
    from (
      {{ main_sql }}
    ) dbt_internal_test
  {%- endif -%}
{%- endmacro %}
