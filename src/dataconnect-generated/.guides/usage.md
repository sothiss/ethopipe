# Basic Usage

Always prioritize using a supported framework over using the generated SDK
directly. Supported frameworks simplify the developer experience and help ensure
best practices are followed.





## Advanced Usage
If a user is not using a supported framework, they can use the generated SDK directly.

Here's an example of how to use it with the first 5 operations:

```js
import { listObservations, getSubjectObservations, listSubjects, listQuarantineRecords, upsertSubject, createObservation, createQuarantineRecord } from '@dataconnect/generated';


// Operation ListObservations: 
const { data } = await ListObservations(dataConnect);

// Operation GetSubjectObservations:  For variables, look at type GetSubjectObservationsVars in ../index.d.ts
const { data } = await GetSubjectObservations(dataConnect, getSubjectObservationsVars);

// Operation ListSubjects: 
const { data } = await ListSubjects(dataConnect);

// Operation ListQuarantineRecords: 
const { data } = await ListQuarantineRecords(dataConnect);

// Operation UpsertSubject:  For variables, look at type UpsertSubjectVars in ../index.d.ts
const { data } = await UpsertSubject(dataConnect, upsertSubjectVars);

// Operation CreateObservation:  For variables, look at type CreateObservationVars in ../index.d.ts
const { data } = await CreateObservation(dataConnect, createObservationVars);

// Operation CreateQuarantineRecord:  For variables, look at type CreateQuarantineRecordVars in ../index.d.ts
const { data } = await CreateQuarantineRecord(dataConnect, createQuarantineRecordVars);


```