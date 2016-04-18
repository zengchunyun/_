/**
 * Created by zengchunyun on 16/4/12.
 */
// var name = "zengchunyun";
// var name = String("zengchunyun");
// var age = String(18);
// // var username = prompt("please input name").trim(); //去除用户输入左右两边空白字符
// console.log(name.charAt(0)); // 获取字符串下标为0的字符
// console.log(name.substring(1,3));  //获取下标>=1 <3的字符
// console.log(name.indexOf('ex'));  //通过字符查找在字符串里的下标,找不到则为-1,如果输入多个字符,则仅返回找到的第一个下标,且字符必须连续
// console.log(name.length);
// var names = ['zeng', 'chun', 'yun'];
// console.log(names);
// var name2 = new Array('zeng', 'chun', 'yun');
// console.log(name2);
// console.log(names.length);  //显示数组长度
// console.log(names[0]); // 显示第一个元素
// names.forEach(function (item, index,array) {
//     console.log(item,index);
// }); //遍历一个数组
//
// names.push('hao'); //将hao元素追加到数组末尾
// console.log(names);
//
// var outobj = names.pop(); //将数组最后一个元素删除并获得被删除的元素
// console.log(outobj,names);
//
// outobj = names.shift();  //删除数组前面的元素,并获得该元素
// console.log(outobj, names);
//
// names.unshift("new"); // 添加元素到数组最前面
// console.log(names);
//
// var ops = names.indexOf("chun");  //找到元素chun在数组中的索引位置
// console.log(ops);
//
//
// names.unshift("new2");
// var removeItem = names.splice(2,1); // 删除下标为2的元素,只删除一次,如果第二个数字1改成2,假如数组索引2后面还有元素,则会将连着的这两个元素一起删除
// console.log(removeItem, '\n',names);
// names.unshift("new3");
// names.unshift("new4");
// names.splice(2,0,'test'); //在第二个元素后的第一个位置插入一个新元素,如果第二位数字是1,则会替换从第一位数字后开始算起的到第二位数,及1这个下标的元素
// console.log(names);
//
// var shallow = names.slice();  //复制数组
// console.log(shallow);
//
// var newsha = names.slice(1,3);  //取>=1 <3的元素给newsha数组,相当于切片
// console.log(newsha,'\n',names);
//
// var newarr = newsha.concat(shallow); //将两个数组合并
// console.log(newarr);
//
// newarr.reverse(); //将数组顺序反转
// console.log(newarr);
//
// var newstr = newarr.join('-'); // 用-拼接元素
// console.log(newstr);
//
// //更多数组介绍https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array

// //普通函数
//     function fus() {
//         console.log('fus');
//         return '222'
//     }
//     var a = fus();
//     console.log(a);
//     function aaa(arg) {
//         console.log(arg);
//     }
//     aaa(222);
// //匿名函数
//     var aas = function (arg) {
//         console.log(arg);
//     };
//     aas(333);
// //自执行函数
//     (function (arg) {
//         console.log(arg)
//     })(223);  //223为参数

// //面向对象
// function MyFoo(name,age) {
//     this.Name = name;
//     this.Age = age;
//     this.Func = function (arg) {
//         return this.Name + arg;
//     }
// }
//
// var obj = new MyFoo('zeng',18);
// var ret = obj.Func('chunyun');
// console.log(ret);

class Polygon {
    constructor(height,width){
        this.height = height;
        this.width = width;
    }
    get area() {
        return this.calcArea()
    }
    calcArea(){
        return this.height * this.width;
    }
}

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    static distance(a, b) {
        const dx = a.x - b.x;
        const dy = a.y - b.y;

        return Math.sqrt(dx*dx + dy*dy);
    }
}

const p1 = new Point(5, 5);
const p2 = new Point(10, 10);

console.log(Point.distance(p1, p2));
//更多介绍https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes