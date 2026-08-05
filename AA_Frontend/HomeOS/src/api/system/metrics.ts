import { api } from "../axiosClient";
import type { Metrics } from "./types.ts";

export const getSystemMetrics = async (): Promise<Metrics> => {
  const response = await api.get(`/system/dashboard/`);
  return response.data;
}