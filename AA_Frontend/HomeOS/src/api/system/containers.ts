import { api } from "../axiosClient";
import type { ContainerStatus } from "./types.ts";

export const getContainersStatus = async (): Promise<ContainerStatus[]> => {
  const response = await api.get(`/system/containers/`);
  return response.data;
}

export const controlContainer = async (container_name: string, action: 'start' | 'stop' | 'restart'): Promise<void> => {
  await api.post(`/system/containers/${container_name}/control/${action}`);
}

export const getContainerLogs = async (container_name: string): Promise<string[]> => {
  const response = await api.get(`/system/containers/${container_name}/logs`);
  return response.data;
}