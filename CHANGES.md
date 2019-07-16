# Connect SDK Changes History

## v16.2

* Catch generic `Exception` on dispatch and skip request instead of aborting execution.
* Insert request id (both tier config or fulfillment) on logs.
* Fix: The `configuration.product.id` and `configuration.account.id` filters do not work as expected. Reverting to `configuration__product__id` and `configuration__account__id`.
* Fix: The SDK was not parsing dropdown value choices correctly.
* Fix: Added `period` field to item.
* Changed documentation theme to sphinx_rtd_theme.

## v16.1

* Fix: Documentation of `FulfillmentAutomation` and `TierConfigAutomation`, and added documentation for `ActivationTemplateResponse` and `ActivationTileResponse`.
* Fix: Return value of `Fulfillment.needs_migration` when migration_info exists but has no value.
* Fix: Some requests are returning params with null values, so support for it has been added.
* Fix: Ensure that the response of an HTTP request is a valid string.
* Fix: Checking for validity of conversation object was done on approval, but not on fail, inquire nor skip.
* Fix: Deserialization of `ServerErrorResponse` in `ApiClient._check_and_pack_response`.

## v16.0

* Feature: Documentation for all SDK classes with examples (and publishing on readthedocs.io).
* Feature: Support for migration from OSA/APS to CB/Connect.
* Feature: Added `@deprecated` decorator.
* Feature: Moved all schemas to internal `connect.models.schemas` package. Deserialization is now done with the `BaseModel.deserialize` method and there are no external references to Marshmallow.
* Feature: Conversation support.
* Fix: Fixed bug when parsing the quantity for an item and the value is 'unlimited'.
* Fix: Connect v16 now includes empty fields as null in the responses instead of omitting them. The SDK now parses these correctly.
* Refactor: Move `get_tier_config` to `TierConfig` class as `get` classmethod.
* Refactor: Refactored exceptions to have more generic names, which allows for these classes to have meaningful names when used outside of the Fulfillment API, and be consistent with package and language standards:
  * FulfillmentFail -> FailRequest
  * FulfillmentInquire -> InquireRequest
  * Skip -> SkipRequest
  * ServerErrorException -> ServerError
* Refactor: Now the SDK is divided into the following subpackages:
  * config
  * exceptions
  * logger
  * models
  * resources
* Refactor: Private methods in UsageAutomation now have a leading underscore, as suggested by PEP-8.

## v15.2

* Feature: `BaseResource.filters` accepts additional filters as optional arguments.
* Feature: `BaseResource.list` accepts an optional dictionary of filters as argument (the one returned by filters method is used as default).
* Fix: Passing of complex data on PUT and POST operations.
* Fix: `TierConfigAutomation.update_parameters`.
* Refactor: `get_tier_config` has moved from `TierConfigAutomation` to `FulfillmentAutomation`.
* Refactor: `BaseResource.config` property now returns the config from the underlying `ApiClient`, instead of storing an additional copy.
* Refactor: `BaseResource.build_filter` has been renamed `BaseResource.filters`. `BaseResource.list` property is now a method.
* Refactor: `BaseResource.api` has been renamed to `BaseResource._api` to suggest private usage by now.
* Refactor: `ApliClient` request methods now return a tuple with the response contents and status code instead of a string.

## v15.1

* Feature: Put proper version into package.

## v15.0

* The production release of connect-python-sdk with support of Connect v15.