import { api } from "../axiosClient";
import type { Log } from "./types.ts";

export const getLogs = async (): Promise<Log[]> => {
  const response = await api.get(`/system/dashboard/logs/`);
  return response.data;
};
