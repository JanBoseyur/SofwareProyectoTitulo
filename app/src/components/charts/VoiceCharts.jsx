
import ReactECharts from "echarts-for-react";

function VoiceChart() {

    const option = {
        backgroundColor: "transparent",

        grid: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0,
            containLabel: false
        },

        tooltip: {
            show: false
        },

        xAxis: {
            type: "category",
            show: false,
            boundaryGap: false,
            axisLabel: { show: false },
            axisLine: { show: false },
            axisTick: { show: false }
        },

        yAxis: {
            type: "value",
            show: false,
            axisLabel: { show: false },
            axisLine: { show: false },
            axisTick: { show: false },
            splitLine: { show: false }
        },

        series: [
            {
                name: "Energía",
                type: "line",
                data: [0.2, 0.5, 0.8, 0.6, 0.3, 0.7, 0.2, 0.16, 0.2, 0.5, 0.8, 0.2, 0.5, 0.8, 0.6, 0.3, 0.7, 0.2, 0.16, 0.3, 0.7, 0.2, 0.16, ],

                animationDuration: 3000,

                smooth: true,
                showSymbol: false,

                lineStyle: {
                    color: "#ffffff",
                    width: 3
                },

                itemStyle: {
                    color: "black"
                },

                areaStyle: {
                    color: "#ffffff",
                    opacity: 0.15
                }
            }
        ]
    };

    return (
        <div style={{
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "flex-end",
        }}>
            <ReactECharts
                option={option}
                style={{ width: "100%", height: "20%" }}
                opts={{ renderer: "svg" }}
            />
        </div>
    );
}

export default VoiceChart;