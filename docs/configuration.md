---
layout: default
title: Configuration File Settings
short_title: Configuration
order: 24
---

## Configuration Settings

This module uses the configuration settings described in this section. None of them are required because the underlying code provides sensible details.

## Sample Configuration

```
us-tx-family:
  court list version: B
  max court number: 1000
  court staff version: A
```

## Definitions

| Setting | Description | Values | Default |
|---------|-------------|--------|---------|
| court list version | A simple version identifier for UsTxCourts to determine whether to download and parse the Texas Government Code. UsTxCourts will automatically refresh the list of courts every month. If you need a quicker refresh, set this configuration variable to something other than the default. | string | "B" |
| court staff version | A simple version identifier for UsTxCourtDirectory to determine whether to download and parse the list of court staff. UsTxCourtDirectory will automatically refresh the list of courts every day. If you need a quicker refresh, set this configuration variable to something other than the default. | string | "A" |
| max court number | When UsTxCourts searches the Texas Government Code for legislation authorizing the district courts, this is the highest numbered court the code searches for. | positive int | 1000 |
