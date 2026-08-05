export interface Log {
  id: string;
  created_at: string;
  event_type: string;
  container: string;
  details: string;
}

export type Metrics = {
    "cpu_usage_percent": number,
    "ram_usage_percent": number,
    "ram_used_gb": number,
    "ram_total_gb": number,
    "temperature_c": number,
    "disk_usage_percent": number,
    "network_download_mbs": number,
    "network_upload_mbs": number
}

export type ContainerStatus = {
    "id": number
    "name": string,
    "state": string,
    "status": string,
    "image": string
}