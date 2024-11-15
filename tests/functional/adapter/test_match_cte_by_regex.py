import re

regex_pattern = r"with\s+(\w+)\s+as"

test_sql_query_1 = """
select 1 as foo
union all
select 2 as bar
"""

test_sql_query_cte_1 = """
WITH cte_name AS (
SELECT 1 as foo
UNION ALL
SELECT 2 as bar
)
SELECT * from cte_name
"""

# CTE query with alternate formatting
test_sql_query_cte_2 = """
WITH
cte_name
AS        (
SELECT 1 as foo
UNION ALL
SELECT 2 as bar
)

SELECT
*
from cte_name
"""


# subqeury with a comment that includes the keyword WITH
test_sql_query_w_comment = """
-- even if WITH is in this comment it should match to a subquery

select 1 as foo
union all
select 2 as bar
"""


# subquery with jinja comment
test_sql_query_w_jinja_comment = """
{% lets try a jinja comment %}

select 1 as foo
union all
select 2 as bar
"""


class TestSqlTestsCTEHelperSynapse:
    """Define tests to match test sql queries against the regex configured
    The queries will have all manners of formatting and comments to test
    If the regex matches then it is a sql statement with a CTE,
    otherwise it should not have a CTE.
    """

    def test_sql_should_match_cte(self):
        matched = re.search(regex_pattern, test_sql_query_cte_1, re.IGNORECASE)
        assert matched is not None

    def test_sql_should_match_cte_unformatted(self):
        matched = re.search(regex_pattern, test_sql_query_cte_2, re.IGNORECASE)
        assert matched is not None

    # Subquery assertions
    def test_sql_match_subquery(self):
        matched = re.search(regex_pattern, test_sql_query_1, re.IGNORECASE)
        assert matched is None

    def test_sql_match_subquery_w_comment(self):
        matched = re.search(regex_pattern, test_sql_query_w_comment, re.IGNORECASE)
        assert matched is None

    def test_sql_match_subquery_w_jinja_comment(self):
        matched = re.search(regex_pattern, test_sql_query_w_jinja_comment, re.IGNORECASE)
        assert matched is None
