import Input from '@material-ui/core/Input';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';

import withStyles from '@material-ui/core/styles/withStyles';
import {scaleSequential} from 'd3-scale';
import * as scaleChromatic from 'd3-scale-chromatic';
import React from 'react';
import ColorSchemeLegend from './ColorSchemeLegend';
import {fixInterpolatorName, getInterpolator, interpolators} from "./util";

const styles = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        'flex-direction': 'column',
    },
    formControl: {
        display: 'block',
        margin: theme.spacing(1)
    },

});

function stripInterpolate(name) {
    if (name.startsWith("interpolate")) {
        name = name.substring("interpolate".length);
    }
    return name;
}


class ColorSchemeSelector extends React.PureComponent {
    handleInterpolatorChange = (event) => {
        let name = event.target.value;
        this.props.handleInterpolator({name: name, value: getInterpolator(name)});
    };

    getScale(name) {
        return scaleSequential(scaleChromatic[name]).domain([0, 1]);
    }

    render() {
        const {classes} = this.props;
        let interpolator = fixInterpolatorName(this.props.interpolator.name);
        const width = 174;
        const height = 14;
        return (
            <Select
                input={<Input/>}
                className={classes.select}
                onChange={this.handleInterpolatorChange}
                value={interpolator}
                multiple={false}>
                <MenuItem key="Diverging" value="Diverging" divider disabled>
                    Diverging
                </MenuItem>
                {interpolators['Diverging'].map(item => (
                    <MenuItem title={stripInterpolate(item)} value={item} key={item}>
                        <ColorSchemeLegend width={width}
                                           label={false} height={height}
                                           scale={this.getScale(item)}/>

                    </MenuItem>))}

                <MenuItem key="Sequential (Single Hue)" value="Sequential (Single Hue)" divider disabled>
                    Sequential (Single Hue)
                </MenuItem>
                {interpolators['Sequential (Single Hue)'].map(item => (
                    <MenuItem title={stripInterpolate(item)} value={item} key={item}>
                        <ColorSchemeLegend width={width}
                                           label={false} height={height}
                                           scale={this.getScale(item)}/>
                    </MenuItem>))}

                <MenuItem key="Sequential (Multi-Hue)" value="Sequential (Multi-Hue)" divider disabled>
                    Sequential (Multi-Hue)
                </MenuItem>
                {interpolators['Sequential (Multi-Hue)'].map(item => (
                    <MenuItem title={stripInterpolate(item)} value={item} key={item}>

                        <ColorSchemeLegend width={width}
                                           label={false} height={height}
                                           scale={this.getScale(item)}/>

                    </MenuItem>))}

                <MenuItem key="Cyclical" value="Cyclical" divider disabled>
                    Cyclical
                </MenuItem>
                {interpolators['Cyclical'].map(item => (
                    <MenuItem title={stripInterpolate(item)} value={item} key={item}>
                        <ColorSchemeLegend width={width}
                                           label={false} height={height}
                                           scale={this.getScale(item)}/>
                    </MenuItem>))}


            </Select>
        );
    }

}


export default withStyles(styles)(ColorSchemeSelector);
