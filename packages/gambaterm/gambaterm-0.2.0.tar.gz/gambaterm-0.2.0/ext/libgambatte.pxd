from libcpp.string cimport string

cdef extern from "gambatte.h" namespace "gambatte":
    cdef cppclass GB:
        GB() except +;
        int load(string& romfile, unsigned flags);
        ptrdiff_t runFor(
            unsigned int *videoBuf,
            ptrdiff_t pitch,
	    unsigned int *audioBuf,
            size_t& samples,
        );
        void setInputGetter(GetInput *getInput);
        void setSaveDir(string& sdir);


cdef extern from "input.h" namespace "gambatte":
    cdef cppclass GetInput:
        unsigned int value;
