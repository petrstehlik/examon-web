import { Component, OnInit, OnDestroy } from '@angular/core';
import { environment as env } from 'environments/environment';

import { HSVtoRGB, calcOffset } from 'app/utils/colors';

declare const b4w;
declare const io;
var socket;

@Component({
  selector: 'ex-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent implements OnInit, OnDestroy {

    public colors = [];
    public metrics = [{
            name : "Ambient Temperature",
            value : "Ambient_Temp"
        },
        {
            name : "Package Temperature",
            value : "temp_pkg"
        },
        {
            name : "Power Consumption",
            value : "pow_pkg"
        },
        {
            name : "CPU Load",
            value : "load_core"
        },
        {
            name : "IPS",
            value : "ips"
        }]

    constructor() { }

    ngOnInit() {
        b4w.require("main").reset();

        if (!b4w.module_check("Galileo_main"))
            this.register();
        // import the app module and start the app by calling the init method
        b4w.require("Galileo_main").init();
    }

    /**
     * This is a callback hell, so everything must be in this function
     */
    register() {
        // register the application module
        b4w.register("Galileo_main", function(exports, require) {

        // import modules used by the app
        var m_app       = require("app");
        var m_cfg       = require("config");
        var m_data      = require("data");
        var m_preloader = require("preloader");
        var m_cont      = require("container");
        var m_mouse     = require("mouse");
        var m_scenes    = require("scenes");
        var m_mat       = require("material");

            socket = io(env.ws.host + ':' + env.ws.port + '/render',
                {reconnection:true});
        var node_data = {};
        var active_metric = env.active_metric;
        var active_metric_name = env.active_metric_name;

        socket.on('connect', function() {
            console.debug("Connected");

            socket.emit('subscribe-metric', {metric : active_metric});
        });

        socket.on('initial-data', function(data) {
            console.log("SOCKET DATA", data);

            // Create a deep copy of original data
            let tmp_data = Object.assign({}, node_data);

            node_data = data;

            // We must clear the model
            /*if (Object.keys(tmp_data).length > 0) {
                for (const key of Object.keys(node_data)) {
                    if (key == 'max' || key == 'min')
                        continue;

                    if (key in data) {
                        //color_node(key, {
                        //    min : data['min'],
                        //    max : data['max'],
                        //    value : data[key]['value']
                        //})
                    } else {
                        console.log("cleaning color")
                        var obj = m_scenes.get_object_by_name(key);
                        m_mat.set_diffuse_color(obj, "node", [1, 1, 1]);
                    }
                }
            }*/
        });

        socket.on('error', function(data) {
            console.error("Error occured", data);
        });

        // detect application mode
        var DEBUG = env.production;

        // automatically detect assets path
        var APP_ASSETS_PATH = m_cfg.get_assets_path("Galileo");

        var _selected_obj;
        /**
         * export the method to initialize the app (called at the bottom of this file)
         */
        exports.init = function() {
            m_app.init({
                canvas_container_id: "main_canvas_container",
                callback: init_cb,
                show_fps: !env.production,
                console_verbose: !env.production,
                assets_gzip_available: env.production,
                autoresize: true
            });
        }

        /**
         * callback executed when the app is initialized
         */
        function init_cb(canvas_elem, success) {

            if (!success) {
                console.log("b4w init failure");
                return;
            }

            m_preloader.create_preloader();

            // ignore right-click on the canvas element
            canvas_elem.oncontextmenu = function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            };

            m_data.load(APP_ASSETS_PATH + "Galileo.json", load_cb, (percentage) => {
                m_preloader.update_preloader(percentage);
            });
        }

        /**
         * callback executed when the scene data is loaded
         */
        function load_cb(data_id, success) {
            if (!success) {
                console.log("b4w load failure");
                return;
            }

            m_app.enable_camera_controls();

            // place your code here
            var canvas_elem = m_cont.get_canvas();
            canvas_elem.addEventListener("mousedown", canvas_click, false);
            canvas_elem.addEventListener("touchstart", canvas_click, false);
            document.getElementById("set-metric").addEventListener("click", swichMetric);

            for (const key of Object.keys(node_data)) {
                if (key == 'min' || key == 'max')
                    continue;

                color_node(key, {
                    value : node_data[key]['value'],
                    min : node_data['min'],
                    max : node_data['max']
                })
            }

            // Register the data reception via websocket only when everything is loaded
            socket.on('data', function(data) {
                color_node(data['node'], {
                    value : data['data']['value'],
                    min : data['range']['min'],
                    max : data['range']['max']
                });

                if (!(data['node'] in node_data))
                    node_data[data['node']] = data

                node_data[data['node']]['value'] = data['data']['value'];
                node_data[data['node']]['timestamp'] = data['data']['timestamp'];

                if (_selected_obj && data['node'] == _selected_obj.name) {
                    fillLabel(data['node']);
                }
            });
        }

        /**
         * Color a node based on the payload
         * payload : {
         *      value,
         *      min,
         *      max
         *  }
         */
        function color_node(nodeID, payload) {
            var obj = m_scenes.get_object_by_name(nodeID);

            if (obj == null) {
                console.warn("Node nod found");
                return;
            }

            // Check if node is in node_data
            // Create the node if needed
            if (!(nodeID in node_data)) {
                node_data[nodeID] = {};
            }

            node_data[nodeID]['color_rgb'] = HSVtoRGB(
                (100 - calcOffset(payload['value'], payload['min'], payload['max'])) * 2.5,
                1.0,
                1.0);
                m_mat.set_diffuse_color(obj, "node", [
                    node_data[nodeID]['color_rgb']['r']/255,
                    node_data[nodeID]['color_rgb']['g']/255,
                    node_data[nodeID]['color_rgb']['b']/255,
                ]);
        }

        function canvas_click(e) {
            if (e.preventDefault)
                e.preventDefault();

            var offset = getOffset(document.getElementById("main_canvas_container"));

            // The shift in coords is needed because the canvas is moved from 0,0 position
            var x = m_mouse.get_coords_x(e) - offset['left'];
            var y = m_mouse.get_coords_y(e) - offset['top'];

            var obj = m_scenes.pick_object(x, y);

            highlightNode(obj);
        }

        function highlightNode(obj) {
            if (obj &&
                m_scenes.check_object_by_name(obj.name) &&
                obj.name.slice(0,4) == "node") {
                fillLabel(obj.name);

                if (_selected_obj != obj) {
                    if (_selected_obj)
                            m_scenes.clear_outline_anim(_selected_obj);
                    if (obj)
                        m_scenes.apply_outline_anim_def(obj);
                    _selected_obj = obj;
                }
            } else if (_selected_obj != undefined) {
                m_scenes.clear_outline_anim(_selected_obj);
                hideLabel();
            }
        }

        function swichMetric(e) {
            socket.emit('unsubscribe-metric', {metric : active_metric});
            let sel = <HTMLSelectElement>document.getElementById("select-metric");

            active_metric = sel.value;
            active_metric_name = sel.options[sel.selectedIndex].innerText;

            socket.emit('subscribe-metric', {metric : active_metric});

            for(const key of Object.keys(node_data)) {
                var obj = m_scenes.get_object_by_name(key);

                if (obj != undefined)
                    m_mat.set_diffuse_color(obj, "node", [1, 1, 1]);
            }

            setTimeout(function() {
                for (const key of Object.keys(node_data)) {
                    if (key == 'min' || key == 'max')
                        continue;

                    color_node(key, {
                        value : node_data[key]['value'],
                        min : node_data['min'],
                        max : node_data['max']
                    })
                }

            }, 1000);
        }

        function fillLabel(node) {
            let label = document.getElementById("label");

            showLabel();

            if (node in node_data) {
                let color = node_data[node]['color_rgb'];
                label.innerHTML = "<h4>Node: " + node + "</h4>" +
                    active_metric_name + ": " + node_data[node]['value'].toFixed(2);
                if (color != undefined) {
                    label.innerHTML += "<span class='color-bar' style='background-color: rgb(" +
                        (color['r']) + "," +
                        (color['g']) + "," +
                        (color['b']) + ");'></span>";
                }

                if (!env.production) {
                    label.innerHTML += "<small>Time of last value: " + new Date(+node_data[node]['timestamp'] * 1000) + "</small>";
                }

            } else {
                label.innerHTML = "<h4>Node: " + node + "</h4><p>No data available</p>";
            }
        }

        function hideLabel() {
            var label = document.getElementById('label');

            label.classList.add("hide")
        }
        function showLabel() {
            var label = document.getElementById('label');

            label.classList.remove("hide")
        }

        // https://stackoverflow.com/questions/442404/retrieve-the-position-x-y-of-an-html-element
        function getOffset( el ) {
            var _x = 0;
            var _y = 0;
            while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
                        _x += el.offsetLeft - el.scrollLeft;
                        _y += el.offsetTop - el.scrollTop;
                        el = el.offsetParent;
                    }
            return { top: _y, left: _x };
        }


        });
    }

    ngOnDestroy() {
        console.log("bye bye");
    }

}
