// import { SVD } from 'svd-js'

class Corrector {

    constructor() {
        this._path = "./autocorrector.txt"
        this._data = new Array();
        return this;
    }

    _readData() {
        return this._data;
    }

    _saveData(data) {
        let numID = data.img_id;
        let pose = data.pose;
        let poseGT = data.poseGt;

        let newData = [numID, pose.x, pose.y, pose.z, poseGT.x, poseGT.y, poseGT.z]
        this._data.push(newData)
    }

    _average(data) {
        var sum = 0;
        for (let i = 0; i < data.length; i++)
            sum += parseInt(data[i], 10);
        return sum / data.length
    }

    _calculateCovar(data) {
        return Math.covariance(data);
    }

    _calculateSVD(matrix) {
        return SVDJS.SVD(matrix)
    }

    correct(newData) {
        this._saveData(newData)
        var data = this._readData()
        var mX = this._average(data.x) 
        var mY = this._average(data.y)
        var mZ = this._average(data.z)

        var data2
        data2.x = data.x - mX
        data2.y = data.y - mY
        data2.z = data.z - mZ

        var covariance = this._calculateCovar(data2)
        var svd = this._calculateSVD(covariance)
        var pca = svd.V // V matrix
        var newDataset = data * svd.V // need matrix operator "@ in python"
    }

    evaluate(newdata) {
        return this._data;
    }

}