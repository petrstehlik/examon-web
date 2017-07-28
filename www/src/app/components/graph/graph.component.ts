declare const Dygraph;

import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// We need labels div reference outside the class since it is need in a callback function
// outside the component class
var labelsDiv : ElementRef = null;

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
        if (data != undefined && data != {}) {
            console.log(Object.assign({}, data));
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

    @Input() title = "Untitled Chart";
    @Input() labels = ["Date"];
    @Input() labelY = "Untitled Y axis";

    @ViewChild('chart') chart : ElementRef;
    @ViewChild('chartLabels') labelsDivRef : ElementRef;

    private graphRef;
    private config : Object;
    constructor(private http : HttpClient) { }

    ngOnInit() {
        this.initConfig();
        labelsDiv = this.labelsDivRef;
    }

    private initConfig() {
        this.config = {
            labels : this.labels,
            hideOverlayOnMouseOut : true,
            ylabel: this.labelY,
            title : this.title,
            legend: 'follow',
            labelsDiv : this.labelsDivRef.nativeElement,
            highlightCallback : this.moveLabel,
            gridLineColor : "rgb(242, 242, 242)",
            highlightCircleSize: 2,
            strokeWidth: 1,
            strokeBorderWidth : 1,
            highlightSeriesOpts: {
              strokeWidth: 2,
              strokeBorderWidth: 0,
              highlightCircleSize: 2
            }
        }
    }

    private moveLabel(event, x, points, row, seriesName) {
        console.log(points);
        console.log(row);
        labelsDiv.nativeElement.style.display = "block";
        labelsDiv.nativeElement.style.left = (event.clientX + 5) + "px";
        labelsDiv.nativeElement.style.top = (event.clientY + 5) + "px";
    }

    private legendFormatter(data) : void {
        return data;
    }

    private extractData(raw : Object) : Array<any> {
        return raw["queries"][0]["results"][0]["values"];
    }


}
