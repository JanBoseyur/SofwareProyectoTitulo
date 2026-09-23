
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
                
                data: [
                    0.03, 0.07, 0.12, 0.09, 0.21,
                    0.36, 0.29, 0.48, 0.62, 0.55,
                    0.71, 0.64, 0.82, 0.68, 0.51,
                    0.43, 0.57, 0.39, 0.24, 0.31,
                    0.18, 0.09, 0.05, 0.08, 0.14,
                    0.27, 0.45, 0.38, 0.61, 0.76,
                    0.69, 0.87, 0.73, 0.58, 0.66,
                    0.49, 0.35, 0.42, 0.28, 0.17,
                    0.11, 0.06, 0.13, 0.22, 0.34,
                    0.29, 0.47, 0.63, 0.52, 0.71
                ],

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

        <div style = {{
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "flex-end",
        }}>
            <ReactECharts
                option = {option}
                style = {{ width: "100%", height: "20%" }}
                opts = {{ renderer: "svg" }}
            />
        </div>
    );
}

export default VoiceChart;