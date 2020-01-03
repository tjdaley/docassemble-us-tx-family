---
layout: default
title: Variables
short_title: Variables
order: 20
---

The **docassemble-us-tx-family** module defines or uses the following variables:

### case

**case** - The current legal case. Instance of *Case*
**case.case_id** - The cause number
**case.country** - "USA"
**case.county** - The name of the county this case will be or was filed in.
**case.court** - Instance of *Court*
**case.court.jurisdiction** - A list containing in 'Texas'. This covers what I think is a bug in the docassemble base code or compensates for something I don't understand. *See*, ```Case.case_id_in_caption()```.
**case.court.name** - "District"
**case.court_number** - Set to the number of the Judicial District that is handling this case.
**case.firstParty** - Is set to ```case.petitioner```.
**case.footer** - An abbreviated version of the case title for document footers. For example, a case entitled "In the Matter of the Marriage of Jane Doe and John Doe" might use "IMMO DOE AND DOE" as the case footer. This is freeform text that is substituted in to the document footers.
**case.petitioner** - A list of petitioners. In your forms, you'll probably expect one petitioner and therefore you'll probably want to use ```${case.petitioner[0].name}```. (Note the array index.)
**case.respondent** - A list of respondents. In your forms, you'll probably expect one respondent and therefore you'll probably want to use ```${case.respondent[0].name}```. (Note the array index.)
**case.secondParty** - Is set to ```case.respondent```.
**case.state** - The political subdivision defining the jurisdiction of the case, i.e. "TEXAS"

### child or children

**child** - A list of children pertaining to this case. Instance of *ChildList*, which is a list of instances of *Individual*.
**child[i]** - This is how an individual child is referenced.

Each child has these properties:

**child.name.first** - The child's first name
**child.name.middle** - The child's middle name (optional)
**child.name.last** - The child's last name
**child.name.suffix** - The suffix to the child's name, e.g. Jr., Sr., etc. (optional)
**child.gender** - The child's gender. One of ['female', 'male', 'other']
**child.birthdate** - The child's date of birth, datatype: date

### doc

**doc** - The current document. Instance of *LegalPleading*.
**doc.case** - Is set to ```case```.

### jobs

**jobs** is an instance of *JobList*. **jobs** is defined in *employment_questions.yml*. **jobs** extends *DAList* wherein each elementin the list is an instance of **job**. Each job is referenced through an index into **jobs**, e.g. ```jobs[0].employer``` is the employer name for the first job.

**jobs** has a *count* property that can be tested in forms, e.g.:

```
{% if jobs.count > 0 %}
   ${obligor} has the following jobs: ${jobs}.
{% endif %}
```

Each job has these properties:

**job.employer** - The name of the employer or the d/b/a if the person is self-employed.
**job.self_employed** - True if this job represents self-employment, otherwise False.
**job.income.value** - The gross income per period specified in *job.income.period*.
**job.income.period** - The frequency with which the person earns a gross of *job.income.value* in this job. The value stored represents the number of times per year the person receives this much in gross income. For example, 1 means "annually", 12 means "monthly" and 52 means "weekly". One of [1, 12, 24, 26, 52]
**job.union_dues.value** - The amount deducted from *job.income.value* for union dues.
**job.union_dues.period** - The frequency with which union dues are deducted. This is not always the same as *job.income.period* because some people with union jobs are paid multiple times per month but their union dues are only withheld once a month. The value stored represents the number of times per year union dues are withheld. For example, 1 means "annually", 12 means "monthly" and 52 means "weekly". One of [1, 12, 24, 26, 52]

### obligor

**obligor** - Set equal to either case.respondent[0] or case.petitioner[0]
**obligor_role** - Indicates whether it is the petitioner or respondent who is the obligor. One of ['P', 'R']
