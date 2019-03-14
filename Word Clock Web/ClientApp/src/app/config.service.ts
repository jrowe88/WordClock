import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

export interface Config {
  color: string;
  option: string;
  pinClock: number;
  pinData: number;
}
export interface ConfigValue {
  key: string;
  value: string;
}

@Injectable()
export class ConfigService {
  constructor(private http: HttpClient) {}

  configUrl = 'http://localhost:5000/api/Config/';

  setValue(key: string, value: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };

    var cfg: ConfigValue = { key: key, value: value };
    return this.http.put<ConfigValue>(this.configUrl, cfg, httpOptions);
  }

  getValue(key: string) {
    return this.http.get<ConfigValue>(this.configUrl + key);
  }
}
