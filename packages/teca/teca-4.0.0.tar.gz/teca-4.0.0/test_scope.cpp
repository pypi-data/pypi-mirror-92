
struct A
{
    using data_t = double;
    data_t foo() { return 1; }
};


struct B
{
    using data_t = float;
    data_t foo() { return 1; }
};


void go()
{
    A a;
    A::data_t va = a.foo();

    B b;
    B::data_t vb = b.foo();

}





