---
tags: component customization, ui design, outsystems ui, api documentation, events handling
summary: Explore the features and API of the Rating component in OutSystems 11 (O11) for mobile and reactive web apps.
locale: en-us
guid: cde868f5-0402-49de-8c91-0754724634cc
app_type: mobile apps, reactive web apps
platform-version: o11
figma: https://www.figma.com/file/eFWRZ0nZhm5J5ibmKMak49/Reference?type=design&node-id=1324%3A1568&mode=design&t=Cx8ecjAITJrQMvRn-1
audience:
  - mobile developers
  - frontend developers
  - full stack developers
  - ui designers
outsystems-tools:
  - service studio
coverage-type:
  - remember
---

# Rating

<div class="info" markdown="1">

Applies to Mobile Apps and Reactive Web Apps only

</div>

## Events

|**Event** |**Output**|**Description**|
|---|---|---|
|OnSelect: Optional |Value (Decimal)|  Event that returns the current rating value. |
  
## Structure

![Diagram illustrating the structure of the Rating component in a mobile or reactive web app](images/rating-diag.png "Rating Component Structure")

<div class="info" markdown="1">

These elements are multiplied by the number of elements in the **RatingScale** input parameter of the **Rating** block.

</div>

### Modifiers

|**Modifier**|**Attribute**|**Element**|
|---|---|---|
|IsEdit|.is-edit|.rating|
|RatingSmall|.rating-small|.rating|
|RatingMedium|.rating-medium|.rating|
|Size|--rating-size|.rating-item|

## API

If you are an advanced user, you might want to use our Rating API (OutSystems.OSUI.Patterns.RatingAPI)for more complex use cases.

### Methods

|**Function**|**Description**|**Parameters**|
|---|---|---|
|ChangeProperty|Changes the Rating property.|<ul><li>ratingId: string</li><li>propertyName: string</li><li>propertyValue: any</li></ul>|
|Create|Creates a new Rating instance and adds it to the ratingMap.|<ul><li>ratingId: string</li><li>configs: string</li></ul>|
|Destroy|Destroys the Rating instance.|<ul><li>ratingId: string</li></ul>|
|GetAllRatings|Returns the Map with all the Rating instances on the screen.|<ul><li>Returns array of Ids</li></ul>|
|GetRatingById|Gets the Rating instance Id.|<ul><li>ratingId: string</li></ul>|
|Initialize|Initializes the pattern instance.|<ul><li> ratingId: string</li></ul>|
