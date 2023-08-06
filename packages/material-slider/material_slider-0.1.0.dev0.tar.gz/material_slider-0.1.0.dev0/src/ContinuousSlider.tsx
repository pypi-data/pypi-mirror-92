import React from 'react';
import Slider from '@material-ui/core/Slider';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

type MyProps = {
    value: number;
    width: string;
    marks: {value: number, label: string}[];
    title: string;
    min: number;
    max: number;
    step: number;
    handleChange: (val: number) => void;
};

type MyState = {
    value: number;
}

export default class ContinuousSlider extends React.Component<MyProps, MyState> {

    constructor(props: MyProps) {
        super(props);
        this.state = { value: props.value };

        this.changeHandler = this.changeHandler.bind(this);
    };

    changeHandler(event: any, newValue: number | number[]) {
        this.setState({ value: newValue as number });
        this.props.handleChange(newValue as number);
    };

    componentDidUpdate(props: MyProps, states: MyState) {
        if (props.value !== this.props.value) {
            this.setState({ value: this.props.value });
        };
    };

    render() {
        return (
            <div className="dou-slider">
                <Grid container spacing={2} alignItems="center">
                    <Grid item>
                        <Typography gutterBottom>
                            { this.props.title }
                </Typography>
                    </Grid>
                    <Grid item>
                        <Slider id="dou"
                            style={{ width: this.props.width }}
                            value={this.state.value}
                            onChange={this.changeHandler}
                            aria-labelledby="continuous-slider"
                            valueLabelDisplay="on"
                            marks={this.props.marks}
                            min={this.props.min}
                            max={this.props.max}
                            step={this.props.step}
                        />
                    </Grid>
                </Grid>
            </div>);
    };
}