# Connect SDK Changes History

## v18.2

* Fix: Accept rql.Query in resources list method.
* Fix: Bug causing some schemas not parsing all the fields.

## v18.1

* Feature: Allow masking of specified log fields.
* Change: Upgrade pytest to version 4.6.8.
* Fix: Added date to log formatter.

## v18.0

* Feature: Updated models for v18.
* Feature: Add RQL filter support.
* Fix: UsageFileAction's subclass SubmitUsageFile had a rejection note, a parameter which should go in RejectUsageFile instead. 

## v17.6

* Fix: `ServerErrorResponseSchema` has a wrong errors field definition, it must be a list of strings.
* Fix: `function_log` decorator use list comprehension to set a custom formatter for each logging handler configured for the current logger. Changed to a for loop.

## v17.5

* Fix: UsageFileAction's subclass SubmitUsageFile has a rejection note, a parameter which should go in RejectUsageFile instead.

## v17.4

* Fix: Due to a bug the log handler was being added for every request, causing log messages being printed twice on the 2nd requests, thrice on the third request, etc.
* Fix: Some fields cannot be properly parsed because their schemas inherit from Schema instead of BaseSchema.
* Fix: A Conversation should not add a message when it is the same as the latest one added.

## v17.3

* HTTP timeout request to Connect platform should be not less than 300 seconds.
* Accept Usage File is sending wrong parameter in post request.
* Usage processor filter "product__id" is not filtering by product id.
* All fields accept null to avoid parsing errors.

## v17.2

* external_id is sometimes returned as an integer by Connect API, which breaks Python SDK parsing.

## v17.1

* Add custom loggers to the automation classes, that automatically add relevant info of the request being processed. Legacy global logger still working in order to have a context-independent logger.
* Get product templates and configuration params.
* Put each model in its own Python file, to reduce the chance of having circular references on imports.
* Tier requests are not filtering by product id by default.
* Fulfillment assignee not receiving the right type.

## v17.0

* Fixed bugs when listing and working with usage files.
* Directory module.
* Models updated with new fields from v17.

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
