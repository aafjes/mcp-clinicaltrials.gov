# ClinicalTrials.gov API Field Reference

Complete reference for fields available in the ClinicalTrials.gov API v2.

## Study Data Structure

Study records are organized into sections and modules:

```
study
├── protocolSection
│   ├── identificationModule
│   ├── statusModule
│   ├── sponsorCollaboratorsModule
│   ├── oversightModule
│   ├── descriptionModule
│   ├── conditionsModule
│   ├── designModule
│   ├── armsInterventionsModule
│   ├── outcomesModule
│   ├── eligibilityModule
│   ├── contactsLocationsModule
│   └── referencesModule
├── resultsSection (when available)
│   ├── participantFlowModule
│   ├── baselineCharacteristicsModule
│   ├── outcomeMeasuresModule
│   └── adverseEventsModule
├── derivedSection
│   └── miscInfoModule
├── documentSection
│   └── largeDocumentModule
└── hasResults (boolean)
```

## Protocol Section Modules

### identificationModule

Basic study identification:

- `nctId` (string): NCT identifier (e.g., "NCT04267848")
- `nctIdAliases` (array): Previous NCT IDs if study was merged
- `orgStudyIdInfo`
  - `id` (string): Organization's study ID
  - `type` (string): ID type
  - `link` (string): URL to organization's page
- `secondaryIdInfos` (array): Additional identifiers
  - `id` (string): Secondary ID
  - `type` (string): ID type (e.g., "EudraCT Number")
  - `domain` (string): Issuing organization
- `organization`
  - `fullName` (string): Organization name
  - `class` (string): Organization type
- `briefTitle` (string): Short study title
- `officialTitle` (string): Full study title
- `acronym` (string): Study acronym

### statusModule

Study status and dates:

- `statusVerifiedDate` (string): Last verification date (YYYY-MM)
- `overallStatus` (enum): Current status
  - RECRUITING
  - NOT_YET_RECRUITING
  - ACTIVE_NOT_RECRUITING
  - COMPLETED
  - SUSPENDED
  - TERMINATED
  - WITHDRAWN
  - ENROLLING_BY_INVITATION
- `lastKnownStatus` (string): Last known status for non-recruiting studies
- `expandedAccessInfo`
  - `hasExpandedAccess` (boolean)
  - `nctId` (string): NCT ID of expanded access record
- `startDateStruct`
  - `date` (string): Start date (YYYY-MM-DD)
  - `type` (string): ACTUAL or ESTIMATED
- `primaryCompletionDateStruct`
  - `date` (string): Primary completion date
  - `type` (string): ACTUAL or ESTIMATED
- `completionDateStruct`
  - `date` (string): Study completion date
  - `type` (string): ACTUAL or ESTIMATED
- `studyFirstSubmitDate` (string): First submission date
- `studyFirstSubmitQcDate` (string): First QC date
- `studyFirstPostDateStruct`
  - `date` (string): First posted date
  - `type` (string): ACTUAL or ESTIMATED
- `resultsFirstSubmitDate` (string): Results first submitted
- `resultsFirstPostDateStruct`
  - `date` (string): Results first posted
  - `type` (string)
- `lastUpdateSubmitDate` (string): Last update submitted
- `lastUpdatePostDateStruct`
  - `date` (string): Last update posted
  - `type` (string)

### sponsorCollaboratorsModule

Sponsor and collaborator information:

- `responsibleParty`
  - `type` (string): PRINCIPAL_INVESTIGATOR or SPONSOR
  - `investigatorFullName` (string): PI name
  - `investigatorTitle` (string): PI title
  - `investigatorAffiliation` (string): PI institution
- `leadSponsor`
  - `name` (string): Lead sponsor name
  - `class` (string): Sponsor type (INDUSTRY, NIH, FED, OTHER, NETWORK, OTHER_GOV, INDIV)
- `collaborators` (array)
  - `name` (string): Collaborator name
  - `class` (string): Collaborator type

### oversightModule

Oversight and monitoring:

- `oversightHasDmc` (boolean): Has Data Monitoring Committee
- `isFdaRegulatedDrug` (boolean): FDA-regulated drug
- `isFdaRegulatedDevice` (boolean): FDA-regulated device
- `isUnapprovedDevice` (boolean): Unapproved device
- `isPpsd` (boolean): Pediatric post-market surveillance
- `isUsExport` (boolean): US export

### descriptionModule

Study descriptions:

- `briefSummary` (string): Brief summary
- `detailedDescription` (string): Detailed description

### conditionsModule

Conditions being studied:

- `conditions` (array of strings): Medical conditions
- `keywords` (array of strings): Keywords

### designModule

Study design information:

- `studyType` (string): INTERVENTIONAL, OBSERVATIONAL, EXPANDED_ACCESS
- `phases` (array): Study phases
  - EARLY_PHASE1
  - PHASE1
  - PHASE2
  - PHASE3
  - PHASE4
  - NA (Not Applicable)
- `designInfo`
  - `allocation` (string): RANDOMIZED, NON_RANDOMIZED, NA
  - `interventionModel` (string): SINGLE_GROUP, PARALLEL, CROSSOVER, FACTORIAL, SEQUENTIAL
  - `interventionModelDescription` (string): Description
  - `primaryPurpose` (string): TREATMENT, PREVENTION, DIAGNOSTIC, SUPPORTIVE_CARE, SCREENING, HEALTH_SERVICES_RESEARCH, BASIC_SCIENCE, DEVICE_FEASIBILITY, OTHER
  - `observationalModel` (string): For observational studies
  - `timePerspective` (string): For observational studies
  - `maskingInfo`
    - `masking` (string): NONE, SINGLE, DOUBLE, TRIPLE, QUADRUPLE
    - `maskingDescription` (string)
    - `whoMasked` (array): PARTICIPANT, CARE_PROVIDER, INVESTIGATOR, OUTCOMES_ASSESSOR
- `enrollmentInfo`
  - `count` (integer): Number of participants
  - `type` (string): ACTUAL or ESTIMATED
- `bioSpec`
  - `retention` (string): NONE, SAMPLES_WITH_DNA, SAMPLES_WITHOUT_DNA
  - `description` (string)
- `patientRegistry` (boolean): Is patient registry

### armsInterventionsModule

Study arms and interventions:

- `armGroups` (array)
  - `label` (string): Arm label
  - `type` (string): EXPERIMENTAL, ACTIVE_COMPARATOR, PLACEBO_COMPARATOR, SHAM_COMPARATOR, NO_INTERVENTION, OTHER
  - `description` (string): Arm description
  - `interventionNames` (array): Interventions in this arm
- `interventions` (array)
  - `type` (string): DRUG, DEVICE, BIOLOGICAL, PROCEDURE, RADIATION, BEHAVIORAL, GENETIC, DIETARY_SUPPLEMENT, COMBINATION_PRODUCT, DIAGNOSTIC_TEST, OTHER
  - `name` (string): Intervention name
  - `description` (string): Description
  - `armGroupLabels` (array): Associated arms
  - `otherNames` (array): Alternative names

### outcomesModule

Outcome measures:

- `primaryOutcomes` (array)
  - `measure` (string): Outcome measure
  - `description` (string): Description
  - `timeFrame` (string): Time frame
- `secondaryOutcomes` (array)
  - Same structure as primaryOutcomes
- `otherOutcomes` (array)
  - Same structure as primaryOutcomes

### eligibilityModule

Eligibility criteria:

- `eligibilityCriteria` (string): Full criteria text
- `healthyVolunteers` (boolean): Accepts healthy volunteers
- `sex` (string): ALL, FEMALE, MALE
- `genderBased` (boolean): Gender-based eligibility
- `genderDescription` (string): Gender description
- `minimumAge` (string): Minimum age (e.g., "18 Years")
- `maximumAge` (string): Maximum age (e.g., "65 Years")
- `stdAges` (array): Standard age groups
  - CHILD (birth to 17 years)
  - ADULT (18 to 64 years)
  - OLDER_ADULT (65+ years)
- `studyPopulation` (string): For observational studies

### contactsLocationsModule

Contact information and study locations:

- `centralContacts` (array)
  - `name` (string): Contact name
  - `role` (string): Contact role
  - `phone` (string): Phone number
  - `phoneExt` (string): Extension
  - `email` (string): Email address
- `overallOfficials` (array)
  - `name` (string): Official name
  - `affiliation` (string): Affiliation
  - `role` (string): PRINCIPAL_INVESTIGATOR, SUB_INVESTIGATOR, STUDY_CHAIR, STUDY_DIRECTOR
- `locations` (array)
  - `facility` (string): Facility name
  - `status` (string): Recruitment status at this location
  - `city` (string): City
  - `state` (string): State/province
  - `zip` (string): Postal code
  - `country` (string): Country
  - `contacts` (array): Location-specific contacts
  - `geoPoint`
    - `lat` (number): Latitude
    - `lon` (number): Longitude

### referencesModule

Related publications and links:

- `references` (array)
  - `pmid` (string): PubMed ID
  - `type` (string): BACKGROUND, RESULT, DERIVED
  - `citation` (string): Full citation
- `seeAlsoLinks` (array)
  - `label` (string): Link label
  - `url` (string): URL
- `availIpds` (array): Individual participant data sharing
  - `id` (string): IPD ID
  - `type` (string): IPD type
  - `url` (string): URL
  - `comment` (string): Comment

## Derived Section

### miscInfoModule

Computed/derived information:

- `versionHolder` (string): Version timestamp
- `submissionTracking`
  - `firstMcpInfo`
    - `postDateStruct`
      - `date` (string)
  - `estimatedResultsFirstSubmitDate` (string)
- `modelPredictions`
  - `unhealthyAlcoholUseRisk` (number): 0-1 probability
  - `unhealthyDrugUseRisk` (number): 0-1 probability

## Search Parameters Reference

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| query.cond | Conditions/diseases | `Depression` |
| query.term | General keyword search | `diabetes treatment` |
| query.intr | Interventions/treatments | `Pembrolizumab` |
| query.titles | Search in titles | `phase 3 trial` |
| query.outc | Outcome measures | `mortality` |
| query.spons | Sponsors | `Pfizer` |
| query.lead | Lead sponsors | `Mayo Clinic` |
| query.id | NCT identifiers | `NCT04267848` |
| query.patient | Patient-friendly terms | `heart disease` |
| query.locn | Locations | `Boston` |

### Filter Parameters

| Parameter | Description | Values/Example |
|-----------|-------------|----------------|
| filter.overallStatus | Recruitment status | `["RECRUITING"]` |
| filter.geo | Geographic filter | `distance(40.7,-74,50mi)` |
| filter.ids | Specific NCT IDs | `["NCT123", "NCT456"]` |
| filter.advanced | Advanced query | Complex expressions |

### Other Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| fields | Fields to return | All fields |
| sort | Sort order | `["@relevance"]` |
| pageSize | Results per page | 20 (max 1000) |
| pageToken | Pagination token | None |
| countTotal | Count total results | false |
| format | Response format | json |

## Field Selection

To retrieve specific fields only, use the `fields` parameter with pipe-separated field names:

```
fields=NCTId|BriefTitle|Condition|Phase
```

Common field selections:

**Minimal:**
```
NCTId|BriefTitle|OverallStatus
```

**Summary:**
```
NCTId|BriefTitle|OfficialTitle|OverallStatus|Condition|Intervention|Phase|Enrollment|StartDate
```

**Full study details:** Omit fields parameter to get all fields.

## Date Formats

- Study dates: YYYY-MM-DD
- Submission dates: YYYY-MM-DD
- Filter dates: YYYY-MM or YYYY-MM-DD

## Enumeration Values

### Study Status
- RECRUITING
- NOT_YET_RECRUITING
- ACTIVE_NOT_RECRUITING  
- COMPLETED
- SUSPENDED
- TERMINATED
- WITHDRAWN
- ENROLLING_BY_INVITATION
- AVAILABLE
- NO_LONGER_AVAILABLE
- APPROVED_FOR_MARKETING
- WITHHELD
- TEMPORARILY_NOT_AVAILABLE

### Study Type
- INTERVENTIONAL
- OBSERVATIONAL
- EXPANDED_ACCESS
- OBSERVATIONAL_PATIENT_REGISTRY

### Phase
- EARLY_PHASE1
- PHASE1
- PHASE2
- PHASE3
- PHASE4
- NA

### Sponsor/Collaborator Class
- INDUSTRY
- NIH
- FED (Other US Federal)
- OTHER_GOV (Other government)
- OTHER
- NETWORK
- INDIV (Individual)

### Intervention Type
- DRUG
- DEVICE
- BIOLOGICAL
- PROCEDURE
- RADIATION
- BEHAVIORAL
- GENETIC
- DIETARY_SUPPLEMENT
- COMBINATION_PRODUCT
- DIAGNOSTIC_TEST
- OTHER

## Examples

### Get minimal info for many studies
```
fields: ["NCTId", "BriefTitle", "OverallStatus"]
page_size: 100
```

### Get detailed protocol info
```
fields: [
  "NCTId",
  "BriefTitle", 
  "OfficialTitle",
  "BriefSummary",
  "DetailedDescription",
  "Condition",
  "InterventionName",
  "EligibilityCriteria",
  "LocationFacility"
]
```

### Search with geographic filter
```
query_cond: "Breast Cancer"
filter_geo: "distance(40.7128,-74.0060,50mi)"
filter_overallStatus: ["RECRUITING"]
```

## Resources

- [Full API Documentation](https://clinicaltrials.gov/data-api/api)
- [Study Data Structure](https://clinicaltrials.gov/data-api/about-api/study-data-structure)
- [Search Areas Guide](https://clinicaltrials.gov/data-api/about-api/search-areas)
