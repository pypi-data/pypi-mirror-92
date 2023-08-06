// Copyright (c) Dou Du
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import ContinuousSlider from './ContinuousSlider';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class MaterialSliderModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MaterialSliderModel.model_name,
      _model_module: MaterialSliderModel.model_module,
      _model_module_version: MaterialSliderModel.model_module_version,
      _view_name: MaterialSliderModel.view_name,
      _view_module: MaterialSliderModel.view_module,
      _view_module_version: MaterialSliderModel.view_module_version,
      value: 0.0,
      width: "400px",
      marks: [],
      labels: [],
      title: "title",
      min: 0.0,
      max: 100.0,
      step: 1.0,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'MaterialSliderModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'MaterialSliderView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class MaterialSliderView extends DOMWidgetView {
  initialize() {
    this.handleChange = this.handleChange.bind(this);
    this._marks = [];
  }

  render() {
    this.el.classList.add('custom-widget');

    this.model.on('change:value', this.value_changed, this);
    this._value = this.model.get('value');
    this._width = this.model.get('width');
    this._title = this.model.get('title');
    this._min = this.model.get('min');
    this._max = this.model.get('max');
    this._step = this.model.get('step');
    let marks = this.model.get('marks');
    let labels = this.model.get('labels');

    for (var i=0; i < marks.length; i++){
      this._marks.push({value: marks[i], label: labels[i]});
    };

    ReactDOM.render(<ContinuousSlider
      title={this._title}
      width={this._width}
      value={this._value}
      marks={this._marks}
      min={this._min}
      max={this._max}
      step={this._step}
      handleChange={this.handleChange}
    />, this.el);
  }

  events(): { [e: string]: string } {
    return { "reset .MuiSlider-thumb": "set_value" };
  }

  set_value(event: any) {
    this.model.set('value', this._value);
    this.touch();
  }

  handleChange(val: number) {
    this.model.set('value', val);
    this.touch();
  }

  value_changed() {
    // this.el.textContent = this.model.get('value');
    this._value = this.model.get('value');
    console.log("The value has been changed" + this._value);
    ReactDOM.render(<ContinuousSlider
      title={this._title}
      width={this._width}
      value={this._value}
      marks={this._marks}
      min={this._min}
      max={this._max}
      step={this._step}
      handleChange={this.handleChange}
    />, this.el);
  }

  private _value: number;
  private _width: string;
  private _marks: {value: number, label: string}[];
  private _title: string;
  private _min: number;
  private _max: number;
  private _step: number;
}

