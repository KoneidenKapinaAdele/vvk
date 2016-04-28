var vvk = function() {

  this.start = function(toiletIds) {
    toiletIds.forEach(this.addRandomEventToToilet, this);
  };

  this.addRandomEventToToilet = function(toiletId) {
  	window.setTimeout(this.getStateChangeFn(toiletId), this.getRandomDelay(2000, 5000));
  };

  this.getRandomDelay = function(min, max) {
  	return Math.random() * (max - min) + min;
  };

  this.isToiletOccupied = function(toiletId) {
  	return document.getElementById(toiletId).classList.contains("occupied");
  };

  this.getStateChangeFn = function(toiletId) {
  	var that = this;
  	if(this.isToiletOccupied(toiletId)) {
  		return function() { that.changeStateToFree(toiletId); };
  	}
  	return function() { that.changeStateToOccupied(toiletId); };
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