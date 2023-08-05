# IGWN Accounting

This small python package provides tools for accounting for
computing usage on the IGWN Computing Grid.

## Accounting reports

The `igwn-accounting-report` script can be used to generate ASCII-formatted
reports.

### Accounting report format

Accounting reports submitted for inclusion in the IGWN accounting must be in
plain ASCII with the following space-separated columns

```
USERNAME ACCOUNTING_TAG CPU_HOURS YYYY-MM-DD CLUSTER
```

None of the data should include string quotes of any kind, and the `CLUSTER`
string should be pre-registerd with the central IGWN accounting.
For example:

```
duncan.macleod igwn.dev.o4.computing.accounting 12345 2021-01-01 ARCCA-CDF
```
