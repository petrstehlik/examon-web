import { Component, OnInit, OnDestroy } from '@angular/core';
import { environment as env } from 'environments/environment';

declare const b4w;

@Component({
  selector: 'ex-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent implements OnInit, OnDestroy {


    constructor() { }

    ngOnInit() {
        if (!b4w.module_check("Galileo_main"))
            this.register();
         // import the app module and start the app by calling the init method
        //b4w.require("Galileo_main").init();
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
        var m_ver       = require("version");

        var m_anim      = require("animation");
        var m_cont      = require("container");
        var m_mouse     = require("mouse");
        var m_scenes    = require("scenes");
        var m_transform = require("transform");

        // detect application mode
        var DEBUG = env.production;

        // automatically detect assets path
        var APP_ASSETS_PATH = m_cfg.get_assets_path("Galileo");

        /**
         * export the method to initialize the app (called at the bottom of this file)
         */
        exports.init = function() {
            m_app.init({
                canvas_container_id: "main_canvas_container",
                callback: init_cb,
                show_fps: !env.production,
                console_verbose: !env.production,
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

            load();
        }

        /**
         * load the scene data
         */
        function load() {
            m_data.load(APP_ASSETS_PATH + "Galileo.json", load_cb, preloader_cb);
        }

        /**
         * update the app's preloader
         */
        function preloader_cb(percentage) {
            m_preloader.update_preloader(percentage);
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
        }

        function canvas_click(e) {
            if (e.preventDefault)
                e.preventDefault();

            var x = m_mouse.get_coords_x(e);
            var y = m_mouse.get_coords_y(e);

            var obj = m_scenes.pick_object(x, y);

            if (obj) {
                console.log(obj.name);

                let label = document.getElementById("label");

                label.innerText = "Selected node: " + obj.name;
            }
        }


        });
    }

    ngOnDestroy() {
        console.log("bye bye");
        //b4w.require("main").pause();
    }

}
