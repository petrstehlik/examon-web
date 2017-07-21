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

    @Input() data;
    @Input() title;
    @Input() labelY;

    @ViewChild('chart') chart : ElementRef;
    @ViewChild('chartLabels') labelsDivRef : ElementRef;

    private graphRef;

    constructor(private http : HttpClient) { }

    ngOnInit() {

        labelsDiv = this.labelsDivRef;

        this.http.get('/api/kairos/basic').subscribe(
            data => {
                this.data = data;

                let values = this.extractData(this.data);
                let plot_data = [];

                let point = this.data["queries"][0]["results"];

                for (var i = 0; i < values.length; i++) {
                    // Add date
                    let tmp = [];
                    tmp.push(new Date(point[0]["values"][i][0]*1000));

                    for (var j = 0; j < point.length; j++) {
                        tmp.push(point[j]["values"][i][1]);
                    }

                    plot_data.push(tmp);
                }

                let labels = ["Time"]

                for (var i = 0; i < point.length; i++) {
                    labels.push(point[i]["group_by"][0]["group"]["core"])
                }

                this.graphRef = new Dygraph(this.chart.nativeElement, plot_data, {
                    labels : labels,
                    hideOverlayOnMouseOut : true,
                    ylabel: this.labelY,
                    title : this.title,
                    legend: 'follow',
                    labelsDiv : labelsDiv.nativeElement,
                    labelsSeparateLines : true,
                    highlightCallback : this.moveLabel,
                    gridLineColor : "rgb(242, 242, 242)"
                });
            });
    }

    private moveLabel(event, x, points, row, seriesName) {
        labelsDiv.nativeElement.style.display = "block";
        labelsDiv.nativeElement.style.left = (event.clientX + 5) + "px";
        labelsDiv.nativeElement.style.top = (event.clientY + 5) + "px";
    }

    private legendFormatter(data) : void {
        console.log(data);

        if (data.x != undefined) {
            console.log((new Date(data.x)).toISOString());
        }
        return data;
    }

    private extractData(raw : Object) : Array<any> {
        return raw["queries"][0]["results"][0]["values"];
    }


}
