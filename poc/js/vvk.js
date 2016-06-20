var vvk = function() {
  this.totalUsageGauge = null;
  this.totalMsFree = 1;
  this.totalMsOccupied = 1;
  this.clockHours = 6;
  this.occupiedMultiplierByHour = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0.7,
    7: 1.2,
    8: 1.5,
    9: 2.7,
    10: 2.8,
    11: 2.5,
    12: 4.0,
    13: 2.5,
    14: 3.0,
    15: 3.0,
    16: 2.7,
    17: 1.4,
    18: 0.9,
    19: 0.7,
    20: 0.6,
    21: 0.0,
    22: 0.0,
    23: 0.0,
    24: 0.0
  };

  this.start = function(toiletIds) {
    this.initGauges();
    toiletIds.forEach(this.addRandomEventToToilet, this);
    this.startClock();
  };

  this.startClock = function() {
    this.progressClock();
    window.setInterval(this.progressClock.bind(this), 10000);
  };

  this.progressClock = function() {
      this.clockHours++;
      if(this.clockHours > 24) {
        this.clockHours = 1;
        this.totalMsFree = 1;
        this.totalMsOccupied = 1;
      }
      document.getElementById('clock').innerHTML = 'klo ' + this.clockHours + ':00';
  };

  this.initGauges = function() {
      this.totalUsageGauge = new JustGage({
        id: "totalUsageGauge",
        value: 0,
        min: 0,
        max: 100,
        title: "Käyttöaste/vrk"
      });
  };

  this.updateGauge = function() {
    var totalUsage = this.totalMsOccupied / (this.totalMsFree + this.totalMsOccupied) * 100;
    this.totalUsageGauge.refresh(totalUsage);
  };

  this.addRandomEventToToilet = function(toiletId) {
    var delay = this.getRandomDelay(3000, 6000);
    var fn;
    if(this.isNextOccupied()) {
      this.totalMsOccupied += delay;
      fn = this.changeStateToOccupied.bind(this, toiletId);
    }
    else {
      this.totalMsFree += delay;
      fn = this.changeStateToFree.bind(this, toiletId);
    }
    this.updateGauge();

  	window.setTimeout(fn, delay);
  };

  this.isNextOccupied = function() {
    var multiplier = this.occupiedMultiplierByHour[this.clockHours];
    var random = Math.random();
    return (random * multiplier) > 0.5;
  },

  this.getRandomDelay = function(min, max) {
  	return Math.random() * (max - min) + min;
  };

  this.isToiletOccupied = function(toiletId) {
  	return document.getElementById(toiletId).classList.contains("occupied");
  };

  this.changeStateToFree = function(toiletId) {
  	var toiletElem = document.getElementById(toiletId);
  	toiletElem.classList.remove("occupied");
  	toiletElem.classList.add("free");

  	this.addRandomEventToToilet(toiletId);
  };

  this.changeStateToOccupied = function(toiletId) {
  	var toiletElem = document.getElementById(toiletId);
  	toiletElem.classList.remove("free");
  	toiletElem.classList.add("occupied");

  	this.addRandomEventToToilet(toiletId);
  };

};