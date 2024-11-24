import { reactive } from "vue";

const getBus = () => {
    return reactive({
        popupVisible: false,
        position: { top: 100, left: 100 },
        offset: { x: 0, y: 0 },
        isDragging: false,

        togglePopup() {
            this.popupVisible = !this.popupVisible;
        },

        turnOn() {
            this.popupVisible = true;
        },

        startDrag(e) {
            this.isDragging = true;
            this.offset = {
                x: e.clientX - this.position.left,
                y: e.clientY - this.position.top
            };
        },

        onDrag(e) {
            if (this.isDragging) {
                this.position = {
                    top: e.clientY - this.offset.y,
                    left: e.clientX - this.offset.x
                };
            }
        },

        stopDrag() {
            this.isDragging = false;
        }
    });
};

export const eventBusTimer = reactive({
    bus: getBus(),
    project: null,
    actionId: 0,

    open(project) {
        this.project = project;

        this.bus.turnOn();
    },

    update() {
        this.actionId++;
    }
});
