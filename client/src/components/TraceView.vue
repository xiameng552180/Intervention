<template>
    <div class = "content" id = "TraceViewSVG">
        </div>
</template>
<script>
import * as d3 from 'd3';
import NetService from '../services/net-service';
import DataService from '../services/data-service';
import PipeService from '../services/pipe-service'
export default {
    name: 'TraceView',
    data(){
        return {
            width: null,
            height: null,
            svg: null,
            localData: null,
            timeData: null,
            interstingAreas: null,
            range: null,
            low: null,
            high: null,
            ratio: null,
            slow: null,
            fast: null,
            flag: null,
            simMatrix: null,
            allVector: null,

        };
    },
    mounted() {
    this.initialize();
    //  PipeService.$on(PipeService.UPDATE_TRACEVIEW,()=>{
    //         this.data = DataService.data;
    //         this.svg.selectAll('*').remove();
           
    //  })
    },
    methods: {
        initialize(){
            this.width = 1000;
            this.height = 8000;
            this.svg = d3.select('#TraceViewSVG').append('svg')
                         .attr('class', 'd3SVG')
                         .attr('width', this.width)
                         .attr('height', this.height)
        },
        

    }
}
</script>
