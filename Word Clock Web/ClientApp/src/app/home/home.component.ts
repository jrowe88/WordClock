import { Component, ViewContainerRef } from '@angular/core';
import { ColorPickerService } from 'ngx-color-picker';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  constructor(
    public vcRef: ViewContainerRef,
    private cpService: ColorPickerService
  ) {}
}
