# Generated TypeScript README
This README will guide you through the process of using the generated JavaScript SDK package for the connector `example`. It will also provide examples on how to use your generated SDK to call your Data Connect queries and mutations.

***NOTE:** This README is generated alongside the generated SDK. If you make changes to this file, they will be overwritten when the SDK is regenerated.*

# Table of Contents
- [**Overview**](#generated-javascript-readme)
- [**Accessing the connector**](#accessing-the-connector)
  - [*Connecting to the local Emulator*](#connecting-to-the-local-emulator)
- [**Queries**](#queries)
  - [*ListObservations*](#listobservations)
  - [*GetSubjectObservations*](#getsubjectobservations)
  - [*ListSubjects*](#listsubjects)
  - [*ListQuarantineRecords*](#listquarantinerecords)
- [**Mutations**](#mutations)
  - [*UpsertSubject*](#upsertsubject)
  - [*CreateObservation*](#createobservation)
  - [*CreateQuarantineRecord*](#createquarantinerecord)

# Accessing the connector
A connector is a collection of Queries and Mutations. One SDK is generated for each connector - this SDK is generated for the connector `example`. You can find more information about connectors in the [Data Connect documentation](https://firebase.google.com/docs/data-connect#how-does).

You can use this generated SDK by importing from the package `@dataconnect/generated` as shown below. Both CommonJS and ESM imports are supported.

You can also follow the instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#set-client).

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
```

## Connecting to the local Emulator
By default, the connector will connect to the production service.

To connect to the emulator, you can use the following code.
You can also follow the emulator instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#instrument-clients).

```typescript
import { connectDataConnectEmulator, getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
connectDataConnectEmulator(dataConnect, 'localhost', 9399);
```

After it's initialized, you can call your Data Connect [queries](#queries) and [mutations](#mutations) from your generated SDK.

# Queries

There are two ways to execute a Data Connect Query using the generated Web SDK:
- Using a Query Reference function, which returns a `QueryRef`
  - The `QueryRef` can be used as an argument to `executeQuery()`, which will execute the Query and return a `QueryPromise`
- Using an action shortcut function, which returns a `QueryPromise`
  - Calling the action shortcut function will execute the Query and return a `QueryPromise`

The following is true for both the action shortcut function and the `QueryRef` function:
- The `QueryPromise` returned will resolve to the result of the Query once it has finished executing
- If the Query accepts arguments, both the action shortcut function and the `QueryRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Query
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each query. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-queries).

## ListObservations
You can execute the `ListObservations` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listObservations(options?: ExecuteQueryOptions): QueryPromise<ListObservationsData, undefined>;

interface ListObservationsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListObservationsData, undefined>;
}
export const listObservationsRef: ListObservationsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listObservations(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListObservationsData, undefined>;

interface ListObservationsRef {
  ...
  (dc: DataConnect): QueryRef<ListObservationsData, undefined>;
}
export const listObservationsRef: ListObservationsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listObservationsRef:
```typescript
const name = listObservationsRef.operationName;
console.log(name);
```

### Variables
The `ListObservations` query has no variables.
### Return Type
Recall that executing the `ListObservations` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListObservationsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListObservationsData {
  observations: ({
    id: string;
    timestamp: TimestampString;
    location: string;
    latitude?: number | null;
    longitude?: number | null;
    behaviorType: string;
    behaviorValue: string;
    severityScore?: number | null;
    behaviorTypeId?: string | null;
    heartRate?: number | null;
    heartRateUnit: string;
    bodyTemp?: number | null;
    tempUnit: string;
    respiratoryRate?: number | null;
    respiratoryRateUnit: string;
    cortisolLevel?: number | null;
    cortisolUnit: string;
    cortisolMatrix?: string | null;
    observationMethod: string;
    narrative: string;
    subject: {
      id: string;
      species: string;
      dogSizeCategory?: string | null;
    } & Subject_Key;
  } & Observation_Key)[];
}
```
### Using `ListObservations`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listObservations } from '@dataconnect/generated';


// Call the `listObservations()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listObservations();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listObservations(dataConnect);

console.log(data.observations);

// Or, you can use the `Promise` API.
listObservations().then((response) => {
  const data = response.data;
  console.log(data.observations);
});
```

### Using `ListObservations`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listObservationsRef } from '@dataconnect/generated';


// Call the `listObservationsRef()` function to get a reference to the query.
const ref = listObservationsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listObservationsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.observations);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.observations);
});
```

## GetSubjectObservations
You can execute the `GetSubjectObservations` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getSubjectObservations(vars: GetSubjectObservationsVariables, options?: ExecuteQueryOptions): QueryPromise<GetSubjectObservationsData, GetSubjectObservationsVariables>;

interface GetSubjectObservationsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetSubjectObservationsVariables): QueryRef<GetSubjectObservationsData, GetSubjectObservationsVariables>;
}
export const getSubjectObservationsRef: GetSubjectObservationsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getSubjectObservations(dc: DataConnect, vars: GetSubjectObservationsVariables, options?: ExecuteQueryOptions): QueryPromise<GetSubjectObservationsData, GetSubjectObservationsVariables>;

interface GetSubjectObservationsRef {
  ...
  (dc: DataConnect, vars: GetSubjectObservationsVariables): QueryRef<GetSubjectObservationsData, GetSubjectObservationsVariables>;
}
export const getSubjectObservationsRef: GetSubjectObservationsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getSubjectObservationsRef:
```typescript
const name = getSubjectObservationsRef.operationName;
console.log(name);
```

### Variables
The `GetSubjectObservations` query requires an argument of type `GetSubjectObservationsVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetSubjectObservationsVariables {
  subjectId: string;
}
```
### Return Type
Recall that executing the `GetSubjectObservations` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetSubjectObservationsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetSubjectObservationsData {
  observations: ({
    id: string;
    timestamp: TimestampString;
    location: string;
    latitude?: number | null;
    longitude?: number | null;
    behaviorType: string;
    behaviorValue: string;
    severityScore?: number | null;
    behaviorTypeId?: string | null;
    heartRate?: number | null;
    heartRateUnit: string;
    bodyTemp?: number | null;
    tempUnit: string;
    respiratoryRate?: number | null;
    respiratoryRateUnit: string;
    cortisolLevel?: number | null;
    cortisolUnit: string;
    cortisolMatrix?: string | null;
    observationMethod: string;
    narrative: string;
  } & Observation_Key)[];
}
```
### Using `GetSubjectObservations`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getSubjectObservations, GetSubjectObservationsVariables } from '@dataconnect/generated';

// The `GetSubjectObservations` query requires an argument of type `GetSubjectObservationsVariables`:
const getSubjectObservationsVars: GetSubjectObservationsVariables = {
  subjectId: ..., 
};

// Call the `getSubjectObservations()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getSubjectObservations(getSubjectObservationsVars);
// Variables can be defined inline as well.
const { data } = await getSubjectObservations({ subjectId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getSubjectObservations(dataConnect, getSubjectObservationsVars);

console.log(data.observations);

// Or, you can use the `Promise` API.
getSubjectObservations(getSubjectObservationsVars).then((response) => {
  const data = response.data;
  console.log(data.observations);
});
```

### Using `GetSubjectObservations`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getSubjectObservationsRef, GetSubjectObservationsVariables } from '@dataconnect/generated';

// The `GetSubjectObservations` query requires an argument of type `GetSubjectObservationsVariables`:
const getSubjectObservationsVars: GetSubjectObservationsVariables = {
  subjectId: ..., 
};

// Call the `getSubjectObservationsRef()` function to get a reference to the query.
const ref = getSubjectObservationsRef(getSubjectObservationsVars);
// Variables can be defined inline as well.
const ref = getSubjectObservationsRef({ subjectId: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getSubjectObservationsRef(dataConnect, getSubjectObservationsVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.observations);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.observations);
});
```

## ListSubjects
You can execute the `ListSubjects` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listSubjects(options?: ExecuteQueryOptions): QueryPromise<ListSubjectsData, undefined>;

interface ListSubjectsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListSubjectsData, undefined>;
}
export const listSubjectsRef: ListSubjectsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listSubjects(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListSubjectsData, undefined>;

interface ListSubjectsRef {
  ...
  (dc: DataConnect): QueryRef<ListSubjectsData, undefined>;
}
export const listSubjectsRef: ListSubjectsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listSubjectsRef:
```typescript
const name = listSubjectsRef.operationName;
console.log(name);
```

### Variables
The `ListSubjects` query has no variables.
### Return Type
Recall that executing the `ListSubjects` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListSubjectsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListSubjectsData {
  subjects: ({
    id: string;
    species: string;
    dogSizeCategory?: string | null;
  } & Subject_Key)[];
}
```
### Using `ListSubjects`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listSubjects } from '@dataconnect/generated';


// Call the `listSubjects()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listSubjects();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listSubjects(dataConnect);

console.log(data.subjects);

// Or, you can use the `Promise` API.
listSubjects().then((response) => {
  const data = response.data;
  console.log(data.subjects);
});
```

### Using `ListSubjects`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listSubjectsRef } from '@dataconnect/generated';


// Call the `listSubjectsRef()` function to get a reference to the query.
const ref = listSubjectsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listSubjectsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.subjects);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.subjects);
});
```

## ListQuarantineRecords
You can execute the `ListQuarantineRecords` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listQuarantineRecords(options?: ExecuteQueryOptions): QueryPromise<ListQuarantineRecordsData, undefined>;

interface ListQuarantineRecordsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListQuarantineRecordsData, undefined>;
}
export const listQuarantineRecordsRef: ListQuarantineRecordsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listQuarantineRecords(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListQuarantineRecordsData, undefined>;

interface ListQuarantineRecordsRef {
  ...
  (dc: DataConnect): QueryRef<ListQuarantineRecordsData, undefined>;
}
export const listQuarantineRecordsRef: ListQuarantineRecordsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listQuarantineRecordsRef:
```typescript
const name = listQuarantineRecordsRef.operationName;
console.log(name);
```

### Variables
The `ListQuarantineRecords` query has no variables.
### Return Type
Recall that executing the `ListQuarantineRecords` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListQuarantineRecordsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListQuarantineRecordsData {
  quarantineRecords: ({
    id: string;
    rawPayload: string;
    errors: string;
    ingestedAt: TimestampString;
    originalIndex?: number | null;
  } & QuarantineRecord_Key)[];
}
```
### Using `ListQuarantineRecords`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listQuarantineRecords } from '@dataconnect/generated';


// Call the `listQuarantineRecords()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listQuarantineRecords();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listQuarantineRecords(dataConnect);

console.log(data.quarantineRecords);

// Or, you can use the `Promise` API.
listQuarantineRecords().then((response) => {
  const data = response.data;
  console.log(data.quarantineRecords);
});
```

### Using `ListQuarantineRecords`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listQuarantineRecordsRef } from '@dataconnect/generated';


// Call the `listQuarantineRecordsRef()` function to get a reference to the query.
const ref = listQuarantineRecordsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listQuarantineRecordsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.quarantineRecords);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.quarantineRecords);
});
```

# Mutations

There are two ways to execute a Data Connect Mutation using the generated Web SDK:
- Using a Mutation Reference function, which returns a `MutationRef`
  - The `MutationRef` can be used as an argument to `executeMutation()`, which will execute the Mutation and return a `MutationPromise`
- Using an action shortcut function, which returns a `MutationPromise`
  - Calling the action shortcut function will execute the Mutation and return a `MutationPromise`

The following is true for both the action shortcut function and the `MutationRef` function:
- The `MutationPromise` returned will resolve to the result of the Mutation once it has finished executing
- If the Mutation accepts arguments, both the action shortcut function and the `MutationRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Mutation
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each mutation. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-mutations).

## UpsertSubject
You can execute the `UpsertSubject` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
upsertSubject(vars: UpsertSubjectVariables): MutationPromise<UpsertSubjectData, UpsertSubjectVariables>;

interface UpsertSubjectRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpsertSubjectVariables): MutationRef<UpsertSubjectData, UpsertSubjectVariables>;
}
export const upsertSubjectRef: UpsertSubjectRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
upsertSubject(dc: DataConnect, vars: UpsertSubjectVariables): MutationPromise<UpsertSubjectData, UpsertSubjectVariables>;

interface UpsertSubjectRef {
  ...
  (dc: DataConnect, vars: UpsertSubjectVariables): MutationRef<UpsertSubjectData, UpsertSubjectVariables>;
}
export const upsertSubjectRef: UpsertSubjectRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the upsertSubjectRef:
```typescript
const name = upsertSubjectRef.operationName;
console.log(name);
```

### Variables
The `UpsertSubject` mutation requires an argument of type `UpsertSubjectVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpsertSubjectVariables {
  id: string;
  species: string;
  dogSizeCategory?: string | null;
}
```
### Return Type
Recall that executing the `UpsertSubject` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpsertSubjectData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpsertSubjectData {
  subject_upsert: Subject_Key;
}
```
### Using `UpsertSubject`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, upsertSubject, UpsertSubjectVariables } from '@dataconnect/generated';

// The `UpsertSubject` mutation requires an argument of type `UpsertSubjectVariables`:
const upsertSubjectVars: UpsertSubjectVariables = {
  id: ..., 
  species: ..., 
  dogSizeCategory: ..., // optional
};

// Call the `upsertSubject()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await upsertSubject(upsertSubjectVars);
// Variables can be defined inline as well.
const { data } = await upsertSubject({ id: ..., species: ..., dogSizeCategory: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await upsertSubject(dataConnect, upsertSubjectVars);

console.log(data.subject_upsert);

// Or, you can use the `Promise` API.
upsertSubject(upsertSubjectVars).then((response) => {
  const data = response.data;
  console.log(data.subject_upsert);
});
```

### Using `UpsertSubject`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, upsertSubjectRef, UpsertSubjectVariables } from '@dataconnect/generated';

// The `UpsertSubject` mutation requires an argument of type `UpsertSubjectVariables`:
const upsertSubjectVars: UpsertSubjectVariables = {
  id: ..., 
  species: ..., 
  dogSizeCategory: ..., // optional
};

// Call the `upsertSubjectRef()` function to get a reference to the mutation.
const ref = upsertSubjectRef(upsertSubjectVars);
// Variables can be defined inline as well.
const ref = upsertSubjectRef({ id: ..., species: ..., dogSizeCategory: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = upsertSubjectRef(dataConnect, upsertSubjectVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.subject_upsert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.subject_upsert);
});
```

## CreateObservation
You can execute the `CreateObservation` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createObservation(vars: CreateObservationVariables): MutationPromise<CreateObservationData, CreateObservationVariables>;

interface CreateObservationRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateObservationVariables): MutationRef<CreateObservationData, CreateObservationVariables>;
}
export const createObservationRef: CreateObservationRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createObservation(dc: DataConnect, vars: CreateObservationVariables): MutationPromise<CreateObservationData, CreateObservationVariables>;

interface CreateObservationRef {
  ...
  (dc: DataConnect, vars: CreateObservationVariables): MutationRef<CreateObservationData, CreateObservationVariables>;
}
export const createObservationRef: CreateObservationRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createObservationRef:
```typescript
const name = createObservationRef.operationName;
console.log(name);
```

### Variables
The `CreateObservation` mutation requires an argument of type `CreateObservationVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateObservationVariables {
  id: string;
  subjectId: string;
  timestamp: TimestampString;
  location: string;
  latitude?: number | null;
  longitude?: number | null;
  behaviorType: string;
  behaviorValue: string;
  severityScore?: number | null;
  behaviorTypeId?: string | null;
  heartRate?: number | null;
  heartRateUnit: string;
  bodyTemp?: number | null;
  tempUnit: string;
  respiratoryRate?: number | null;
  respiratoryRateUnit: string;
  cortisolLevel?: number | null;
  cortisolUnit: string;
  cortisolMatrix?: string | null;
  observationMethod: string;
  narrative: string;
}
```
### Return Type
Recall that executing the `CreateObservation` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateObservationData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateObservationData {
  observation_insert: Observation_Key;
}
```
### Using `CreateObservation`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createObservation, CreateObservationVariables } from '@dataconnect/generated';

// The `CreateObservation` mutation requires an argument of type `CreateObservationVariables`:
const createObservationVars: CreateObservationVariables = {
  id: ..., 
  subjectId: ..., 
  timestamp: ..., 
  location: ..., 
  latitude: ..., // optional
  longitude: ..., // optional
  behaviorType: ..., 
  behaviorValue: ..., 
  severityScore: ..., // optional
  behaviorTypeId: ..., // optional
  heartRate: ..., // optional
  heartRateUnit: ..., 
  bodyTemp: ..., // optional
  tempUnit: ..., 
  respiratoryRate: ..., // optional
  respiratoryRateUnit: ..., 
  cortisolLevel: ..., // optional
  cortisolUnit: ..., 
  cortisolMatrix: ..., // optional
  observationMethod: ..., 
  narrative: ..., 
};

// Call the `createObservation()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createObservation(createObservationVars);
// Variables can be defined inline as well.
const { data } = await createObservation({ id: ..., subjectId: ..., timestamp: ..., location: ..., latitude: ..., longitude: ..., behaviorType: ..., behaviorValue: ..., severityScore: ..., behaviorTypeId: ..., heartRate: ..., heartRateUnit: ..., bodyTemp: ..., tempUnit: ..., respiratoryRate: ..., respiratoryRateUnit: ..., cortisolLevel: ..., cortisolUnit: ..., cortisolMatrix: ..., observationMethod: ..., narrative: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createObservation(dataConnect, createObservationVars);

console.log(data.observation_insert);

// Or, you can use the `Promise` API.
createObservation(createObservationVars).then((response) => {
  const data = response.data;
  console.log(data.observation_insert);
});
```

### Using `CreateObservation`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createObservationRef, CreateObservationVariables } from '@dataconnect/generated';

// The `CreateObservation` mutation requires an argument of type `CreateObservationVariables`:
const createObservationVars: CreateObservationVariables = {
  id: ..., 
  subjectId: ..., 
  timestamp: ..., 
  location: ..., 
  latitude: ..., // optional
  longitude: ..., // optional
  behaviorType: ..., 
  behaviorValue: ..., 
  severityScore: ..., // optional
  behaviorTypeId: ..., // optional
  heartRate: ..., // optional
  heartRateUnit: ..., 
  bodyTemp: ..., // optional
  tempUnit: ..., 
  respiratoryRate: ..., // optional
  respiratoryRateUnit: ..., 
  cortisolLevel: ..., // optional
  cortisolUnit: ..., 
  cortisolMatrix: ..., // optional
  observationMethod: ..., 
  narrative: ..., 
};

// Call the `createObservationRef()` function to get a reference to the mutation.
const ref = createObservationRef(createObservationVars);
// Variables can be defined inline as well.
const ref = createObservationRef({ id: ..., subjectId: ..., timestamp: ..., location: ..., latitude: ..., longitude: ..., behaviorType: ..., behaviorValue: ..., severityScore: ..., behaviorTypeId: ..., heartRate: ..., heartRateUnit: ..., bodyTemp: ..., tempUnit: ..., respiratoryRate: ..., respiratoryRateUnit: ..., cortisolLevel: ..., cortisolUnit: ..., cortisolMatrix: ..., observationMethod: ..., narrative: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createObservationRef(dataConnect, createObservationVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.observation_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.observation_insert);
});
```

## CreateQuarantineRecord
You can execute the `CreateQuarantineRecord` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createQuarantineRecord(vars: CreateQuarantineRecordVariables): MutationPromise<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;

interface CreateQuarantineRecordRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateQuarantineRecordVariables): MutationRef<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;
}
export const createQuarantineRecordRef: CreateQuarantineRecordRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createQuarantineRecord(dc: DataConnect, vars: CreateQuarantineRecordVariables): MutationPromise<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;

interface CreateQuarantineRecordRef {
  ...
  (dc: DataConnect, vars: CreateQuarantineRecordVariables): MutationRef<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;
}
export const createQuarantineRecordRef: CreateQuarantineRecordRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createQuarantineRecordRef:
```typescript
const name = createQuarantineRecordRef.operationName;
console.log(name);
```

### Variables
The `CreateQuarantineRecord` mutation requires an argument of type `CreateQuarantineRecordVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateQuarantineRecordVariables {
  id: string;
  rawPayload: string;
  errors: string;
  ingestedAt: TimestampString;
  originalIndex?: number | null;
}
```
### Return Type
Recall that executing the `CreateQuarantineRecord` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateQuarantineRecordData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateQuarantineRecordData {
  quarantineRecord_insert: QuarantineRecord_Key;
}
```
### Using `CreateQuarantineRecord`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createQuarantineRecord, CreateQuarantineRecordVariables } from '@dataconnect/generated';

// The `CreateQuarantineRecord` mutation requires an argument of type `CreateQuarantineRecordVariables`:
const createQuarantineRecordVars: CreateQuarantineRecordVariables = {
  id: ..., 
  rawPayload: ..., 
  errors: ..., 
  ingestedAt: ..., 
  originalIndex: ..., // optional
};

// Call the `createQuarantineRecord()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createQuarantineRecord(createQuarantineRecordVars);
// Variables can be defined inline as well.
const { data } = await createQuarantineRecord({ id: ..., rawPayload: ..., errors: ..., ingestedAt: ..., originalIndex: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createQuarantineRecord(dataConnect, createQuarantineRecordVars);

console.log(data.quarantineRecord_insert);

// Or, you can use the `Promise` API.
createQuarantineRecord(createQuarantineRecordVars).then((response) => {
  const data = response.data;
  console.log(data.quarantineRecord_insert);
});
```

### Using `CreateQuarantineRecord`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createQuarantineRecordRef, CreateQuarantineRecordVariables } from '@dataconnect/generated';

// The `CreateQuarantineRecord` mutation requires an argument of type `CreateQuarantineRecordVariables`:
const createQuarantineRecordVars: CreateQuarantineRecordVariables = {
  id: ..., 
  rawPayload: ..., 
  errors: ..., 
  ingestedAt: ..., 
  originalIndex: ..., // optional
};

// Call the `createQuarantineRecordRef()` function to get a reference to the mutation.
const ref = createQuarantineRecordRef(createQuarantineRecordVars);
// Variables can be defined inline as well.
const ref = createQuarantineRecordRef({ id: ..., rawPayload: ..., errors: ..., ingestedAt: ..., originalIndex: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createQuarantineRecordRef(dataConnect, createQuarantineRecordVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.quarantineRecord_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.quarantineRecord_insert);
});
```

