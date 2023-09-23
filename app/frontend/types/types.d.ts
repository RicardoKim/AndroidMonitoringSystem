// types.d.ts
export interface ProcessTableData {
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
      Running: number;
      Sleeping: number;
      Stopped: number;
      Task: number;
      Zombie: number;
      _id: string;
    };
    ns: {
      coll: string;
      db: string;
    };
    operationType: string;
    wallTime: string;
  }
  