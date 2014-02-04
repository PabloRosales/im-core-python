<%inherit file="/core/crud/html/base.mako" />
<style>
    svg {
        display: block;
    }
    #chart svg {
        height: 400px;
        width: 100%;
    }
</style>
<div id="chart">
    <svg></svg>
</div>
<%block name="javascript">
    <script type="text/javascript">

        var data = [{
            key: '${title}',
            values: [
                % for d in data:
                    {
                        x: ${d.label},
                        y: ${d.value}
                    },
                % endfor
            ]
        }];

        nv.addGraph(function(){
            var chart = nv.models.lineWithFocusChart();

            d3.select('#chart svg')
                .datum(data)
                .transition()
                .duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });

    </script>
</%block>
