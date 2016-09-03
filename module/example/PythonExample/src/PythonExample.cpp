#include "PythonExample.h"

#include <Python.h>

#include "extension/Configuration.h"
#include "message/example/ExampleMessage.h"

extern "C" {
    PyObject* PyInit_message();
}
namespace module {
namespace example {

    using extension::Configuration;
    using message::example::ExampleMessage;

    PythonExample::PythonExample(std::unique_ptr<NUClear::Environment> environment)
    : Reactor(std::move(environment)) {


        //  http://stackoverflow.com/questions/26061298/python-multi-thread-multi-interpreter-c-api

        on<Configuration>("PythonExample.yaml").then([this] (const Configuration& config) {
            // Use configuration here from file PythonExample.yaml
        });

        on<Startup>().then([this] {
            PyImport_AppendInittab("message", &PyInit_message);
            Py_Initialize();

            PyRun_SimpleString("from message.example import ExampleMessage\n"
                               "print(__name__)"
                               "print('.' + ExampleMessage.__module__ + '.' + ExampleMessage.__name__)\n"
            );
        });

        on<Every<1, std::chrono::seconds>>().then([this] {
            emit(std::make_unique<ExampleMessage>());
        });

        on<Trigger<ExampleMessage>>().then([this] (const ExampleMessage& msg) {

        });

        on<Shutdown, Priority::LOW>().then(Py_Finalize);
    }
}
}
