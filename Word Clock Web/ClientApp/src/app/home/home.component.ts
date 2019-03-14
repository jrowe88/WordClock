import { Component, OnInit, ViewContainerRef } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ColorPickerService } from 'ngx-color-picker';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { ConfigService } from '../config.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  _config: ConfigService;

  configForm = new FormGroup({
    color: new FormControl(''),
    clockPin: new FormControl(''),
    dataPin: new FormControl(''),
    option: new FormControl('')
  });

  private _success = new Subject<string>();
  selectedColor = '';
  savedMessage = null;
  selectedOption = '';

  ngOnInit(): void {
    this._success.subscribe(message => (this.savedMessage = message));
    this._success
      .pipe(debounceTime(5000))
      .subscribe(() => (this.savedMessage = null));
  }

  constructor(
    public vcRef: ViewContainerRef,
    private cpService: ColorPickerService,
    private config: ConfigService
  ) {
    this._config = config;

    // Get the default color and pin values
    this._config.getValue('color').subscribe(cfg => {
      this.selectedColor = cfg.value;
      this.configForm.patchValue({ color: this.selectedColor });
    });
    this._config
      .getValue('clockPin')
      .subscribe(cfg => this.configForm.patchValue({ clockPin: +cfg.value }));
    this._config
      .getValue('dataPin')
      .subscribe(cfg => this.configForm.patchValue({ dataPin: +cfg.value }));
    this._config.getValue('option').subscribe(cfg => {
      this.configForm.patchValue({ option: +cfg.value });
      this.selectedOption = cfg.value;
    });
  }

  public onSubmit() {
    this.configForm.value.color = this.selectedColor;
    this._config
      .setValue('color', this.configForm.value.color)
      .subscribe(() => {
        this._config
          .setValue('clockPin', this.configForm.value.clockPin.toString())
          .subscribe(() => {
            this._config
              .setValue('dataPin', this.configForm.value.dataPin.toString())
              .subscribe(() => {
                this._config
                  .setValue('option', this.configForm.value.option.toString())
                  .subscribe();
              });
          });
        this._success.next('saved');
      });
  }
}
