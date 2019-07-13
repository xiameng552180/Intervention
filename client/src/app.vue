<template>
    <div class="content">
        <div class = "row">
            <div class = "col-lg-12">
                <trace-view></trace-view>
            </div>
        </div>    
    </div>
</template>

<script>
    import 'bootstrap/dist/css/bootstrap.min.css';
    import TraceView from './components/TraceView';
    import NetService from './services/net-service';
    import DataService from './services/data-service';
    import PipeService from './services/pipe-service';

    export default {
        name: 'App',
        components: {
            TraceView,

        },
        data() {
            return {
               
            };
        },
        mounted() {
            this.$nextTick(function foo() {
                this.initialize();
            });
        },
        methods: {
            initialize() {
                console.log('hello world');
                // NetService.loadData((resp)=>{
                //    // console.log(resp.data)
                //    DataService.data = resp.data
                //    PipeService.$emit(PipeService.UPDATE_TRACEVIEW)
                // })
            },
        },
    };
</script>

<style scoped>
.col-lg-9 {
    padding-right: 0px;
    padding-left: 0px;
}
.container {
        width: 95%;
        margin: auto; 
        background: repeating-linear-gradient(45deg, #eee, #eee 10px, #eee 10px, #eee 20px);
    }

    p {
        display: inline-block;
    }

    .window {
        margin: 8px 4px 0px 4px;
        padding: 0px 0px 0px 0px;
        box-shadow: 0px 1px 1px #666;
        background-color: #ffffff;
        border-color: #ffffff;
        border-width: 1px;
        border-style: solid;
        border-radius: 2px; }
        .window .title {
            padding: 1px 2px 1px 2px;
            font-size: 16px;
            color: #000;
            border-color: #666;
            border-style: solid;
            font-weight: 600;
            border-width: 0px 0px 1px 0px; }
        .window .content {
            background-color: #ffffff;
            border-radius: 3px;
            padding: 5px;
            overflow-x: auto;
            overflow-y: auto; }
            .window .content .filter {
            width: 100%;
            font-size: 14px;
            margin: 2px 0px 0px 0px; }
            .window .content .filter select {
                width: 240px; }
            .window .content .filter .select2-container {
                font-size: 16px; }
                .window .content .filter .select2-container .select2-selection {
                min-height: 20px; }
            .window .content .filter .select2-container--default .select2-selection--multiple .select2-selection__choice {
                margin-top: 2px;
                margin-right: 2px; }
        .window .controls {
            padding: 5px;
            font-size: 16px; }
        .window .icon-fold-up {
            float: right;
            font-size: 10px; }

</style>

