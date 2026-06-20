import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, ExecuteQueryOptions, MutationRef, MutationPromise, DataConnectSettings } from 'firebase/data-connect';

export const connectorConfig: ConnectorConfig;
export const dataConnectSettings: DataConnectSettings;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;




export interface CreateObservationData {
  observation_insert: Observation_Key;
}

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

export interface CreateQuarantineRecordData {
  quarantineRecord_insert: QuarantineRecord_Key;
}

export interface CreateQuarantineRecordVariables {
  id: string;
  rawPayload: string;
  errors: string;
  ingestedAt: TimestampString;
  originalIndex?: number | null;
}

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

export interface GetSubjectObservationsVariables {
  subjectId: string;
}

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

export interface ListQuarantineRecordsData {
  quarantineRecords: ({
    id: string;
    rawPayload: string;
    errors: string;
    ingestedAt: TimestampString;
    originalIndex?: number | null;
  } & QuarantineRecord_Key)[];
}

export interface ListSubjectsData {
  subjects: ({
    id: string;
    species: string;
    dogSizeCategory?: string | null;
  } & Subject_Key)[];
}

export interface Observation_Key {
  id: string;
  __typename?: 'Observation_Key';
}

export interface QuarantineRecord_Key {
  id: string;
  __typename?: 'QuarantineRecord_Key';
}

export interface Subject_Key {
  id: string;
  __typename?: 'Subject_Key';
}

export interface UpsertSubjectData {
  subject_upsert: Subject_Key;
}

export interface UpsertSubjectVariables {
  id: string;
  species: string;
  dogSizeCategory?: string | null;
}

interface ListObservationsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListObservationsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListObservationsData, undefined>;
  operationName: string;
}
export const listObservationsRef: ListObservationsRef;

export function listObservations(options?: ExecuteQueryOptions): QueryPromise<ListObservationsData, undefined>;
export function listObservations(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListObservationsData, undefined>;

interface GetSubjectObservationsRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetSubjectObservationsVariables): QueryRef<GetSubjectObservationsData, GetSubjectObservationsVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetSubjectObservationsVariables): QueryRef<GetSubjectObservationsData, GetSubjectObservationsVariables>;
  operationName: string;
}
export const getSubjectObservationsRef: GetSubjectObservationsRef;

export function getSubjectObservations(vars: GetSubjectObservationsVariables, options?: ExecuteQueryOptions): QueryPromise<GetSubjectObservationsData, GetSubjectObservationsVariables>;
export function getSubjectObservations(dc: DataConnect, vars: GetSubjectObservationsVariables, options?: ExecuteQueryOptions): QueryPromise<GetSubjectObservationsData, GetSubjectObservationsVariables>;

interface ListSubjectsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListSubjectsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListSubjectsData, undefined>;
  operationName: string;
}
export const listSubjectsRef: ListSubjectsRef;

export function listSubjects(options?: ExecuteQueryOptions): QueryPromise<ListSubjectsData, undefined>;
export function listSubjects(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListSubjectsData, undefined>;

interface ListQuarantineRecordsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListQuarantineRecordsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListQuarantineRecordsData, undefined>;
  operationName: string;
}
export const listQuarantineRecordsRef: ListQuarantineRecordsRef;

export function listQuarantineRecords(options?: ExecuteQueryOptions): QueryPromise<ListQuarantineRecordsData, undefined>;
export function listQuarantineRecords(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListQuarantineRecordsData, undefined>;

interface UpsertSubjectRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpsertSubjectVariables): MutationRef<UpsertSubjectData, UpsertSubjectVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpsertSubjectVariables): MutationRef<UpsertSubjectData, UpsertSubjectVariables>;
  operationName: string;
}
export const upsertSubjectRef: UpsertSubjectRef;

export function upsertSubject(vars: UpsertSubjectVariables): MutationPromise<UpsertSubjectData, UpsertSubjectVariables>;
export function upsertSubject(dc: DataConnect, vars: UpsertSubjectVariables): MutationPromise<UpsertSubjectData, UpsertSubjectVariables>;

interface CreateObservationRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateObservationVariables): MutationRef<CreateObservationData, CreateObservationVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateObservationVariables): MutationRef<CreateObservationData, CreateObservationVariables>;
  operationName: string;
}
export const createObservationRef: CreateObservationRef;

export function createObservation(vars: CreateObservationVariables): MutationPromise<CreateObservationData, CreateObservationVariables>;
export function createObservation(dc: DataConnect, vars: CreateObservationVariables): MutationPromise<CreateObservationData, CreateObservationVariables>;

interface CreateQuarantineRecordRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateQuarantineRecordVariables): MutationRef<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateQuarantineRecordVariables): MutationRef<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;
  operationName: string;
}
export const createQuarantineRecordRef: CreateQuarantineRecordRef;

export function createQuarantineRecord(vars: CreateQuarantineRecordVariables): MutationPromise<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;
export function createQuarantineRecord(dc: DataConnect, vars: CreateQuarantineRecordVariables): MutationPromise<CreateQuarantineRecordData, CreateQuarantineRecordVariables>;

