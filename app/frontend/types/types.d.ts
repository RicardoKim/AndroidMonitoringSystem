// types.d.ts
export interface ResourceTableType {
    _id: {
      _data: string;
    };
    clusterTime: {
      T: number;
      I: number;
    };
    documentKey: {
      _id: string;
    };
    fullDocument: {
      created_at: string;
      memory_info: number[];
      cpu_usage: number;
      battery_level: number;
    };
    ns: {
      coll: string;
      db: string;
    };
    operationType: string;
    wallTime: string;
  }

