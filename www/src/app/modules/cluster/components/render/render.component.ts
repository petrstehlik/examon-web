import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { environment as env } from 'environments/environment';

import { HSVtoRGB, calcOffset, getOffset } from 'app/utils/colors';
import { metrics } from './metrics';

declare const io;
let active_metric = env.active_metric;
let active_metric_name = env.active_metric_name;

@Component({
  selector: 'ex-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent implements OnInit, OnDestroy {

    public colors = [];
    public metrics = metrics;
    private socket;
    public data = {};
    public range = {};

    public cluster = [
        ['davide0', 'davide1', 'davide2', 'davide3', 'davide4', 'davide5', 'davide6', 'davide7', 'davide8', 'davide9','davide10', 'davide11', 'davide12', 'davide13', 'davide14'],
        ['davide15', 'davide16', 'davide17', 'davide18', 'davide19', 'davide20', 'davide21', 'davide22', 'davide23', 'davide24','davide25', 'davide26', 'davide27', 'davide28', 'davide29'],
        ['davide30', 'davide31', 'davide32', 'davide33', 'davide34', 'davide35', 'davide36', 'davide37', 'davide38', 'davide39','davide40', 'davide41', 'davide42', 'davide43', 'davide44'],
        ];

    constructor() { }

    ngOnInit() {
        this.connect();
        this.subscribe();
        this.initialData();
        this.receiveData();
    }

    /**
     * Connect to a websocket and register callback for errors
      */
    private connect() {
        this.socket = io(env.ws.host + ':' + env.ws.port + '/render', { reconnection: true });

        this.socket.on('connect', function() {
            console.info('connected to WebSocket server');
        });

        this.socket.on('error', function(data) {
            console.error('Error occured', data);
        });
    }

    /**
     * subscribe to a selected metric
     *
     * @param {string} metric
     */
    public subscribe(metric = active_metric) {
        this.socket.emit('unsubscribe-metric', {metric: active_metric})
        active_metric = metric;
        this.socket.emit('subscribe-metric', {metric : metric});
        this.data = {}
    }

    private initialData() {
        this.socket.on('initial-data', (data) => {
            console.log(data);
            this.data = data;
            this.range = {
                min: data['min'],
                max: data['max'],
            };

            for (let node in data) {
                if (node != 'min' && node != 'max') {
                    this.color_node(node, data[node]['value'])
                }
            }
        });
    }

    private receiveData() {
        this.socket.on('data', (data) => {
            this.data[data['node']] = data['data'];
            this.range = data['range'];
            this.color_node(data['node'], data['data']['value'])
        })
    }

    /**
     * This is a callback hell, so everything must be in this function
     */
    //    let node_data = {};

    //    let _selected_obj;

    //

    //    socket.on('initial-data', function(data) {
    //        // Create a deep copy of original data
    //        const tmp_data = Object.assign({}, node_data);

    //        node_data = data;

    //        // We must clear the model
    //        if (Object.keys(tmp_data).length > 0) {
    //            for (const key of Object.keys(tmp_data)) {
    //                if (key === 'max' || key === 'min') {
    //                    continue;
    //                }

    //                const obj = m_scenes.get_object_by_name(key);
    //                m_mat.set_diffuse_color(obj, 'node', [1, 1, 1]);
    //            }

    //            for (const key of Object.keys(node_data)) {
    //                if (key === 'min' || key === 'max') {
    //                    continue;
    //                }

    //                color_node(key, {
    //                    value : node_data[key]['value'],
    //                    min : node_data['min'],
    //                    max : node_data['max']
    //                });
    //            }
    //        }
    //    });

    //        const sel = <HTMLSelectElement>document.getElementById('select-metric');

    //        sel.value = active_metric;

    //        document.getElementById('set-metric').addEventListener('click', swichMetric);

    //        // Model is initialized so we can color the nodes
    //        for (const key of Object.keys(node_data)) {
    //            if (key === 'min' || key === 'max') {
    //                continue;
    //            }

    //            color_node(key, {
    //                value : node_data[key]['value'],
    //                min : node_data['min'],
    //                max : node_data['max']
    //            });
    //        }

    //        // Register the data reception via websocket only when everything is loaded
    //        socket.on('data', function(data) {
    //            if (!(data['node'] in node_data)) {
    //                node_data[data['node']] = data;
    //            }

    //            node_data[data['node']]['value'] = data['data']['value'];
    //            node_data[data['node']]['timestamp'] = data['data']['timestamp'];

    //            color_node(data['node'], {
    //                value : data['data']['value'],
    //                min : data['range']['min'],
    //                max : data['range']['max']
    //            });

    //            if (_selected_obj && data['node'] === _selected_obj.name) {
    //                fillLabel(data['node']);
    //            }
    //        });
    //    }

    //    /**
    //     * Color a node based on the payload
    //     * payload : {
    //     *      value,
    //     *      min,
    //     *      max
    //     *  }
    //     */
    //    function color_node(nodeID, payload) {
    //        const obj = m_scenes.get_object_by_name(nodeID);

    //        if (obj == null) {
    //            console.warn('Node nod found');
    //            return;
    //        }

    //        // Check if node is in node_data
    //        // Create the node if needed
    //        if (!(nodeID in node_data)) {
    //            node_data[nodeID] = {};
    //        }

    //        node_data[nodeID]['color_rgb'] = HSVtoRGB(
    //            (100 - calcOffset(payload['value'], payload['min'], payload['max'])) * 2.5,
    //            1.0,
    //            1.0);
    //            m_mat.set_diffuse_color(obj, 'node', [
    //                node_data[nodeID]['color_rgb']['r'] / 255,
    //                node_data[nodeID]['color_rgb']['g'] / 255,
    //                node_data[nodeID]['color_rgb']['b'] / 255,
    //            ]);
    //    }

    //    function canvas_click(e) {
    //        if (e.preventDefault) {
    //            e.preventDefault();
    //        }

    //        const offset = getOffset(document.getElementById('main_canvas_container'));

    //        // The shift in coords is needed because the canvas is moved from 0,0 position
    //        const x = m_mouse.get_coords_x(e) - offset['left'];
    //        const y = m_mouse.get_coords_y(e) - offset['top'];

    //        const obj = m_scenes.pick_object(x, y);

    //        highlightNode(obj);
    //    }

    //    function highlightNode(obj) {
    //        if (obj &&
    //            m_scenes.check_object_by_name(obj.name) &&
    //            obj.name.slice(0, 4) === 'node') {
    //            fillLabel(obj.name);

    //            if (_selected_obj != obj) {
    //                if (_selected_obj)
    //                        m_scenes.clear_outline_anim(_selected_obj);
    //                if (obj)
    //                    m_scenes.apply_outline_anim_def(obj);
    //                _selected_obj = obj;
    //            }
    //        } else if (_selected_obj != undefined) {
    //            m_scenes.clear_outline_anim(_selected_obj);
    //            hideLabel();
    //        }
    //    }

    //    function swichMetric(e) {
    //        if (_selected_obj) {
    //            m_scenes.clear_outline_anim(_selected_obj);
    //        }
    //        _selected_obj = null;
    //        socket.emit('unsubscribe-metric', {metric : active_metric});
    //        const sel = <HTMLSelectElement>document.getElementById('select-metric');

    //        active_metric = sel.value;
    //        active_metric_name = sel.options[sel.selectedIndex].innerText;

    //        socket.emit('subscribe-metric', {metric : active_metric});
    //    }

    //    function fillLabel(node) {
    //        const label = document.getElementById('label');

    //        showLabel();

    //        if (node in node_data) {
    //            const color = node_data[node]['color_rgb'];
    //            label.innerHTML = '<h4>Node: ' + node + '</h4>' +
    //                active_metric_name + ': ' + node_data[node]['value'].toFixed(2);
    //            if (color !== undefined) {
    //                label.innerHTML += '<span class=\'color-bar\' style=\'background-color: rgb(' +
    //                    (color['r']) + ',' +
    //                    (color['g']) + ',' +
    //                    (color['b']) + ');\'></span>';
    //            }

    //            if (!env.production) {
    //                label.innerHTML += '<small>Time of last value: ' + new Date//(+node_data[node]['timestamp'] * 1000) + '</small>';
    //            }

    //        } else {
    //            label.innerHTML = '<h4>Node: ' + node + '</h4><p>No data available</p>';
    //        }
    //    }

    //    function hideLabel() {
    //        const label = document.getElementById('label');

    //        label.classList.add('hide');
    //    }
    //    function showLabel() {
    //        const label = document.getElementById('label');

    //        label.classList.remove('hide');
    //    }
    //});
    //}

    private color_node(nodeID, value) {

            // Check if node is in node_data
            // Create the node if needed
            if (!(nodeID in this.data)) {
                this.data[nodeID] = {};
            }

            this.data[nodeID]['color_rgb'] = HSVtoRGB(
                (100 - calcOffset(value, this.range['min'], this.range['max'])) * 2.5,
                1.0,
                1.0);
        }

    private unsubscribe() {
        console.debug('unsubscribing from WS')
        this.socket.emit('unsubscribe-metric', {metric : active_metric});
        this.socket.disconnect();
    }

    ngOnDestroy() {
        this.unsubscribe();
    }

    @HostListener('window:beforeunload', [ '$event' ])
    beforeUnloadHandler(event) {
        this.unsubscribe();
    }

}
