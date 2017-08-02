declare const Dygraph;

import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment as env } from 'environments/environment';

@Component({
  selector: 'ex-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {

    /**
     * Data to render in the graph
     *
     * The data item is expected to have the first item in array a Date object
     *
     * format: {
     *      "labels" : [],
     *      "data" : []
     * }
     */
    private data : Object;

    @Input('data')
    set setData(data) {
        if (data != undefined && Object.keys(data).length !== 0) {
            this.data = data;
            if (this.graphRef == undefined) {
                this.config["labels"] = this.data["labels"];

                this.graphRef = new Dygraph(
                    this.chart.nativeElement,
                    this.data["data"],
                    this.config);
            } else {
                this.graphRef.updateOptions({
                    file : this.data["data"],
                    labels : this.data["labels"]
                });
            }
        }
    };

    @Input('loading') loading : boolean;

    @Input() topTitle = "Untitled Chart";
    @Input() labels = ["Date"];
    @Input() labelY = "Untitled Y axis";

    // The trick with 100.5 is to display the 100 tick in the graph
    @Input() range = [0,100.5];

    // Set height of chart's div so the chart itself will resize to it
    @Input() height = env.chart.height;

    @Input() stacked : boolean = false;

    @ViewChild('chart') chart : ElementRef;
    @ViewChild('chartLabels') labelsDivRef : ElementRef;

    private graphRef;
    private config : Object;

    constructor(private http : HttpClient) { }

    ngOnInit() {
        this.initConfig();
    }

    private initConfig() {
        this.config = {
            labels : this.labels,
            hideOverlayOnMouseOut : true,
            ylabel: this.labelY,
            title : this.topTitle,
            legend: 'follow',
            labelsDiv : this.labelsDivRef.nativeElement,
            highlightCallback : this.moveLabel,
            gridLineColor : "rgb(242, 242, 242)",
            highlightCircleSize: 2,
            strokeWidth: 1,
            strokeBorderWidth : 1,
            valueRange : this.range,
            stackedGraph : this.stacked,
            highlightSeriesOpts: {
              strokeWidth: 2,
              strokeBorderWidth: 0,
              highlightCircleSize: 2
            }
        }
    }

    public moveLabel(event, x, points, row, seriesName) {
        // Use event's DOM to find the labels div to operate with
        // This way we can have multiple graphs on the same page
        let label = (event.composedPath())[1].lastChild

        // Set styles
        label.style.display = "block";
        label.style.left = (event.clientX + env.chart.labels.offsetX) + "px";
        label.style.top = (event.clientY + env.chart.labels.offsetY) + "px";
    }

    private legendFormatter(data) : void {
        return data;
    }

    private extractData(raw : Object) : Array<any> {
        return raw["queries"][0]["results"][0]["values"];
    }


}
