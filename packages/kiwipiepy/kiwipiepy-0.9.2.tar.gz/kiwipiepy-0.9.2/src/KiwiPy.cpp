#include <stdexcept>

#ifdef _DEBUG
#undef _DEBUG
#include "PyDoc.h"
#define _DEBUG
#else 
#include "PyDoc.h"
#endif

#include "core/Kiwi.h"

using namespace std;
using namespace kiwi;

struct UniquePyObj
{
	PyObject* obj;
	UniquePyObj(PyObject* _obj = nullptr) : obj(_obj) {}
	~UniquePyObj()
	{
		Py_XDECREF(obj);
	}

	UniquePyObj(const UniquePyObj&) = delete;
	UniquePyObj& operator=(const UniquePyObj&) = delete;

	UniquePyObj(UniquePyObj&& o)
	{
		std::swap(obj, o.obj);
	}

	UniquePyObj& operator=(UniquePyObj&& o)
	{
		std::swap(obj, o.obj);
		return *this;
	}

	PyObject* get() const
	{
		return obj;
	}

	operator bool() const
	{
		return !!obj;
	}

	operator PyObject*() const
	{
		return obj;
	}
	};

string getModuleFilename(PyObject* moduleObj)
{
	if (!moduleObj) throw bad_exception{};
	UniquePyObj filePath = PyModule_GetFilenameObject(moduleObj);
	if (!filePath) throw bad_exception{};
	string spath = PyUnicode_AsUTF8(filePath);
	return spath;
}

static PyObject* gModule;

struct KiwiObject
{
	PyObject_HEAD;
	Kiwi* inst;
	bool owner;

	static void dealloc(KiwiObject* self)
	{
		delete self->inst;
		Py_TYPE(self)->tp_free((PyObject*)self);
	}

	static int init(KiwiObject *self, PyObject *args, PyObject *kwargs)
	{
		const char* modelPath = nullptr;
		size_t numThreads = 0, options = 3;
		static const char* kwlist[] = { "num_workers", "model_path", "options", nullptr };
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|nzn", (char**)kwlist, &numThreads, &modelPath, &options)) return -1;
		try
		{
			string spath;
			if (modelPath)
			{
				spath = modelPath;
				if (spath.back() != '/' || spath.back() != '\\') spath.push_back('/');
			}
			else
			{
				UniquePyObj modelModule = PyImport_ImportModule("kiwipiepy_model");
				if (!modelModule) throw bad_exception{};
				spath = getModuleFilename(modelModule);
				spath = spath.substr(0, (spath.rfind('/') != spath.npos ? spath.rfind('/') : spath.rfind('\\')) + 1);
			}

			self->inst = new Kiwi{ spath.c_str(), 0, numThreads, options };
			return 0;
		}
		catch (const bad_exception&)
		{
		}
		catch (const exception& e)
		{
			cerr << e.what() << endl;
			PyErr_SetString(PyExc_Exception, e.what());
		}
		return -1;
	}
};

static PyObject* kiwi__addUserWord(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__analyze(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__async_analyze(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__extractAddWords(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__extractFilterWords(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__extractWords(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__loadUserDictionary(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__perform(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__prepare(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__setCutOffThreshold(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__get_option(KiwiObject* self, PyObject* args, PyObject *kwargs);
static PyObject* kiwi__set_option(KiwiObject* self, PyObject* args, PyObject *kwargs);

static PyMethodDef Kiwi_methods[] =
{
	{ "addUserWord", (PyCFunction)kiwi__addUserWord, METH_VARARGS | METH_KEYWORDS, Kiwi_addUserWord__doc__ },
	{ "add_user_word", (PyCFunction)kiwi__addUserWord, METH_VARARGS | METH_KEYWORDS, Kiwi_add_user_word__doc__ },
	{ "loadUserDictionary", (PyCFunction)kiwi__loadUserDictionary, METH_VARARGS | METH_KEYWORDS, Kiwi_loadUserDictionary__doc__ },
	{ "load_user_dictionary", (PyCFunction)kiwi__loadUserDictionary, METH_VARARGS | METH_KEYWORDS, Kiwi_load_user_dictionary__doc__ },
	{ "extractWords", (PyCFunction)kiwi__extractWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extractWords__doc__ },
	{ "extract_words", (PyCFunction)kiwi__extractWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extract_words__doc__ },
	{ "extractFilterWords", (PyCFunction)kiwi__extractFilterWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extractFilterWords__doc__ },
	{ "extract_filter_words", (PyCFunction)kiwi__extractFilterWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extract_filter_words__doc__ },
	{ "extractAddWords", (PyCFunction)kiwi__extractAddWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extractAddWords__doc__ },
	{ "extract_add_words", (PyCFunction)kiwi__extractAddWords, METH_VARARGS | METH_KEYWORDS, Kiwi_extract_add_words__doc__ },
	{ "perform", (PyCFunction)kiwi__perform, METH_VARARGS | METH_KEYWORDS, Kiwi_perform__doc__ },
	{ "setCutOffThreshold", (PyCFunction)kiwi__setCutOffThreshold, METH_VARARGS | METH_KEYWORDS, Kiwi_setCutoffThreshold__doc__ },
	{ "set_cutoff_threshold", (PyCFunction)kiwi__setCutOffThreshold, METH_VARARGS | METH_KEYWORDS, Kiwi_set_cutoff_threshold__doc__ },
	{ "prepare", (PyCFunction)kiwi__prepare, METH_VARARGS | METH_KEYWORDS, Kiwi_prepare__doc__ },
	{ "analyze", (PyCFunction)kiwi__analyze, METH_VARARGS | METH_KEYWORDS, Kiwi_analyze__doc__ },
	{ "get_option", (PyCFunction)kiwi__get_option, METH_VARARGS | METH_KEYWORDS, Kiwi_get_option__doc__ },
	{ "set_option", (PyCFunction)kiwi__set_option, METH_VARARGS | METH_KEYWORDS, Kiwi_set_option__doc__ },
	{ "async_analyze", (PyCFunction)kiwi__async_analyze, METH_VARARGS | METH_KEYWORDS, Kiwi_async_analyze__doc__ },
	{ nullptr }
};

static PyObject* kiwi__version(KiwiObject* self, void* closure);

static PyGetSetDef Kiwi_getsets[] = 
{
	{ (char*)"version", (getter)kiwi__version, nullptr, "get version", nullptr },
	{ nullptr },
};

static PyTypeObject Kiwi_type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"kiwipiepy.Kiwi",             /* tp_name */
	sizeof(KiwiObject), /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)KiwiObject::dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,   /* tp_flags */
	Kiwi__doc__,           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	Kiwi_methods,             /* tp_methods */
	0,						 /* tp_members */
	Kiwi_getsets,        /* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)KiwiObject::init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
};

PyObject* resToPyList(const vector<KResult>& res)
{
	PyObject* retList = PyList_New(res.size());
	size_t idx = 0;
	for (auto& p : res)
	{
		PyObject* rList = PyList_New(p.first.size());
		size_t jdx = 0;
		size_t u32offset = 0;
		for (auto& q : p.first)
		{
			size_t u32chrs = 0;
			for (auto u : q.str())
			{
				if ((u & 0xFC00) == 0xD800) u32chrs++;
			}

			PyList_SetItem(rList, jdx++, Py_BuildValue("(ssnn)", Kiwi::toU8(q.str()).c_str(), tagToString(q.tag()), (size_t)q.pos() - u32offset, (size_t)q.len() - u32chrs));
			u32offset += u32chrs;
		}
		PyList_SetItem(retList, idx++, Py_BuildValue("(Nf)", rList, p.second));
	}
	return retList;
}

struct KiwiAwaitableRes
{
	PyObject_HEAD;
	KiwiObject* kiwi;
	future<vector<KResult>> fut;

	static void dealloc(KiwiAwaitableRes* self)
	{
		Py_XDECREF(self->kiwi);
		Py_TYPE(self)->tp_free((PyObject*)self);
	}

	static int init(KiwiAwaitableRes *self, PyObject *args, PyObject *kwargs)
	{
		KiwiObject* kiwi;
		static const char* kwlist[] = { "kiwi", nullptr };
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", (char**)kwlist, &kiwi)) return -1;
		try
		{
			self->kiwi = kiwi;
			Py_INCREF(kiwi);
		}
		catch (const exception& e)
		{
			cerr << e.what() << endl;
			PyErr_SetString(PyExc_Exception, e.what());
			return -1;
		}
		return 0;
	}

	static PyObject* get(KiwiAwaitableRes *self, PyObject*, PyObject*);
};

static PyTypeObject KiwiAwaitableRes_type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"kiwipiepy._awaitable_res",             /* tp_name */
	sizeof(KiwiAwaitableRes), /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)KiwiAwaitableRes::dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_as_async */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	(ternaryfunc)KiwiAwaitableRes::get,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,   /* tp_flags */
	"",           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	0,             /* tp_methods */
	0,						 /* tp_members */
	0,        /* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)KiwiAwaitableRes::init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
};

PyObject* KiwiAwaitableRes::get(KiwiAwaitableRes *self, PyObject*, PyObject*)
{
	return resToPyList(self->fut.get());
}

static PyObject* kiwi__async_analyze(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topN = 1, matchOptions = PatternMatcher::all;
	char* text;
	static const char* kwlist[] = { "text", "top_n", "match_options", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|nn", (char**)kwlist, &text, &topN, &matchOptions)) return nullptr;
	try
	{
		auto fut = self->inst->asyncAnalyze(text, topN, matchOptions);
		UniquePyObj args = Py_BuildValue("(O)", self);
		PyObject* ret = PyObject_CallObject((PyObject*)&KiwiAwaitableRes_type, args);
		((KiwiAwaitableRes*)ret)->fut = move(fut);
		return ret;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
	}
	return nullptr;
}


struct KiwiResIter
{
	PyObject_HEAD;
	KiwiObject* kiwi;
	PyObject* inputIter;
	size_t topN, matchOptions;
	deque<future<vector<KResult>>> futures;

	static void dealloc(KiwiResIter* self)
	{
		Py_XDECREF(self->kiwi);
		Py_XDECREF(self->inputIter);
		self->futures.~deque();
		Py_TYPE(self)->tp_free((PyObject*)self);
	}

	static int init(KiwiResIter* self, PyObject* args, PyObject* kwargs)
	{
		KiwiObject* kiwi;
		PyObject* ii;
		static const char* kwlist[] = { "kiwi", "ii", nullptr };
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", (char**)kwlist, &kiwi, &ii)) return -1;
		try
		{
			self->kiwi = kiwi;
			Py_INCREF(kiwi);
			self->inputIter = ii;
			Py_INCREF(ii);
			new (&self->futures) deque<future<vector<KResult>>>;
		}
		catch (const exception& e)
		{
			PyErr_SetString(PyExc_Exception, e.what());
			return -1;
		}
		return 0;
	}

	static KiwiResIter* iter(KiwiResIter* self)
	{
		Py_INCREF(self);
		return self;
	}

	bool feed_next_input()
	{
		PyObject* item = PyIter_Next(inputIter);
		if (!item) return false;
		if (!PyUnicode_Check(item)) throw runtime_error{ "`analyze` requires a `str` or an iterable of `str` parameters." };
		futures.emplace_back(kiwi->inst->asyncAnalyze(PyUnicode_AsUTF8(item), topN, matchOptions));
		Py_DECREF(item);
		return true;
	}

	static PyObject* iternext(KiwiResIter* self)
	{
		try
		{
			if (!self->feed_next_input() && self->futures.empty()) return nullptr;

			auto f = move(self->futures.front());
			self->futures.pop_front();
			auto res = f.get();
			if (res.size() > self->topN) res.erase(res.begin() + self->topN, res.end());
			return resToPyList(res);
		}
		catch (const bad_exception&)
		{
		}
		catch (const exception& e)
		{
			PyErr_SetString(PyExc_Exception, e.what());
		}
		return nullptr;
	}
};

static PyTypeObject KiwiResIter_type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"kiwipiepy._res_iter",             /* tp_name */
	sizeof(KiwiResIter), /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)KiwiResIter::dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_as_async */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,   /* tp_flags */
	"",           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	(getiterfunc)KiwiResIter::iter,                         /* tp_iter */
	(iternextfunc)KiwiResIter::iternext,                         /* tp_iternext */
	0,             /* tp_methods */
	0,						 /* tp_members */
	0,        /* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)KiwiResIter::init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
};


static PyObject* kiwi__addUserWord(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	const char* word;
	const char* tag = "NNP";
	float score = 0;
	static const char* kwlist[] = { "word", "tag", "score", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|sf", (char**)kwlist, &word, &tag, &score)) return nullptr;
	try
	{
		return Py_BuildValue("n", self->inst->addUserWord(Kiwi::toU16(word), makePOSTag(Kiwi::toU16(tag)), score));
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* kiwi__loadUserDictionary(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	const char* path;
	static const char* kwlist[] = { "dict_path", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", (char**)kwlist, &path)) return nullptr;
	try
	{
		return Py_BuildValue("n", self->inst->loadUserDictionary(path));
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* kiwi__extractWords(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argReader;
	size_t minCnt = 10, maxWordLen = 10;
	float minScore = 0.25f;
	static const char* kwlist[] = { "reader", "min_cnt", "max_word_len", "min_score", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|nnf", (char**)kwlist, &argReader, &minCnt, &maxWordLen, &minScore)) return nullptr;
	if (!PyCallable_Check(argReader)) return PyErr_SetString(PyExc_TypeError, "extractWords requires 1st parameter which is callable"), nullptr;
	try
	{
		auto res = self->inst->extractWords([argReader](size_t id) -> u16string
		{
			UniquePyObj argList = Py_BuildValue("(n)", id);
			UniquePyObj retVal = PyEval_CallObject(argReader, argList);
			if (!retVal) throw bad_exception();
			if (PyObject_Not(retVal))
			{
				return {};
			}
			if (!PyUnicode_Check(retVal)) throw runtime_error{ "reader must return a value in 'str' type" };
			auto utf8 = PyUnicode_AsUTF8(retVal);
			if (!utf8) throw bad_exception();
			return Kiwi::toU16(utf8);
		}, minCnt, maxWordLen, minScore);

		PyObject* retList = PyList_New(res.size());
		size_t idx = 0;
		for (auto& r : res)
		{
			auto v = Py_BuildValue("(sfnf)", Kiwi::toU8(r.form).c_str(), r.score, r.freq, r.posScore[KPOSTag::NNP]);
			if (!v) throw bad_exception();
			PyList_SetItem(retList, idx++, v);
		}
		return retList;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* kiwi__extractFilterWords(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argReader;
	size_t minCnt = 10, maxWordLen = 10;
	float minScore = 0.25f, posScore = -3;
	static const char* kwlist[] = { "reader", "min_cnt", "max_word_len", "min_score", "pos_score", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|nnff", (char**)kwlist, &argReader, &minCnt, &maxWordLen, &minScore, &posScore)) return nullptr;
	if (!PyCallable_Check(argReader)) return PyErr_SetString(PyExc_TypeError, "extractFilterWords requires 1st parameter which is callable"), nullptr;
	try
	{
		auto res = self->inst->extractWords([argReader](size_t id) -> u16string
		{
			UniquePyObj argList = Py_BuildValue("(n)", id);
			UniquePyObj retVal = PyEval_CallObject(argReader, argList);
			if (!retVal) throw bad_exception();
			if (PyObject_Not(retVal))
			{
				return {};
			}
			if (!PyUnicode_Check(retVal)) throw runtime_error{ "reader must return a value in 'str' type" };
			auto utf8 = PyUnicode_AsUTF8(retVal);
			if (!utf8) throw bad_exception();
			return Kiwi::toU16(utf8);
		}, minCnt, maxWordLen, minScore);

		res = self->inst->filterExtractedWords(move(res), posScore);
		PyObject* retList = PyList_New(res.size());
		size_t idx = 0;
		for (auto& r : res)
		{
			PyList_SetItem(retList, idx++, Py_BuildValue("(sfnf)", Kiwi::toU8(r.form).c_str(), r.score, r.freq, r.posScore[KPOSTag::NNP]));
		}
		return retList;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* kiwi__extractAddWords(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argReader;
	size_t minCnt = 10, maxWordLen = 10;
	float minScore = 0.25f, posScore = -3;
	static const char* kwlist[] = { "reader", "min_cnt", "max_word_len", "min_score", "pos_score", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|nnff", (char**)kwlist, &argReader, &minCnt, &maxWordLen, &minScore, &posScore)) return nullptr;
	if (!PyCallable_Check(argReader)) return PyErr_SetString(PyExc_TypeError, "extractAddWords requires 1st parameter which is callable"), nullptr;
	try
	{
		auto res = self->inst->extractAddWords([argReader](size_t id) -> u16string
		{
			UniquePyObj argList = Py_BuildValue("(n)", id);
			UniquePyObj retVal = PyEval_CallObject(argReader, argList);
			if (!retVal) throw bad_exception();
			if (PyObject_Not(retVal))
			{
				return {};
			}
			if (!PyUnicode_Check(retVal)) throw runtime_error{ "reader must return a value in 'str' type" };
			auto utf8 = PyUnicode_AsUTF8(retVal);
			if (!utf8) throw bad_exception();
			return Kiwi::toU16(utf8);
		}, minCnt, maxWordLen, minScore, posScore);

		PyObject* retList = PyList_New(res.size());
		size_t idx = 0;
		for (auto& r : res)
		{
			PyList_SetItem(retList, idx++, Py_BuildValue("(sfnf)", Kiwi::toU8(r.form).c_str(), r.score, r.freq, r.posScore[KPOSTag::NNP]));
		}
		return retList;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* kiwi__setCutOffThreshold(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	float threshold;
	static const char* kwlist[] = { "threshold", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "f", (char**)kwlist, &threshold)) return nullptr;
	try
	{
		self->inst->setCutOffThreshold(threshold);
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* kiwi__prepare(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	static const char* kwlist[] = { nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", (char**)kwlist)) return nullptr;
	try
	{
		return Py_BuildValue("n", self->inst->prepare());
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* kiwi__get_option(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	ssize_t option;
	static const char* kwlist[] = { "option", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "n", (char**)kwlist, &option)) return nullptr;
	try
	{
		return Py_BuildValue("n", self->inst->getOption(option));
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* kiwi__set_option(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	ssize_t option, value;
	static const char* kwlist[] = { "option", "value", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "nn", (char**)kwlist, &option, &value)) return nullptr;
	try
	{
		self->inst->setOption(option, value);
		Py_INCREF(Py_None);
		return Py_None;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* kiwi__analyze(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topN = 1, matchOptions = PatternMatcher::all;
	{
		PyObject* text;
		static const char* kwlist[] = { "text", "top_n", "match_options", nullptr };
		if (PyArg_ParseTupleAndKeywords(args, kwargs, "O|nn", (char**)kwlist, &text, &topN, &matchOptions))
		{
			try
			{
				if (PyUnicode_Check(text))
				{
					auto res = self->inst->analyze(PyUnicode_AsUTF8(text), max(topN, (size_t)10), matchOptions);
					if (res.size() > topN) res.erase(res.begin() + topN, res.end());
					return resToPyList(res);
				}
				else
				{
					UniquePyObj iter = PyObject_GetIter(text);
					if (!iter) throw runtime_error{ "`analyze` requires a `str` or an iterable of `str` parameters." };
					KiwiResIter* ret = (KiwiResIter*)PyObject_CallFunctionObjArgs((PyObject*)&KiwiResIter_type, (PyObject*)self, iter.get(), nullptr);
					if (!ret) return nullptr;
					ret->topN = topN;
					ret->matchOptions = matchOptions;
					for (int i = 0; i < self->inst->getNumThreads() * 16; ++i)
					{
						if (!ret->feed_next_input()) break;
					}
					return (PyObject*)ret;
				}
			}
			catch (const exception& e)
			{
				PyErr_SetString(PyExc_Exception, e.what());
				return nullptr;
			}
		}
		PyErr_Clear();
	}
	{
		PyObject* reader, *receiver;
		static const char* kwlist[] = { "reader", "receiver", "top_n", "match_options", nullptr };
		if (PyArg_ParseTupleAndKeywords(args, kwargs, "OO|nn", (char**)kwlist, &reader, &receiver, &topN, &matchOptions))
		{
			try
			{
				if (!PyCallable_Check(reader)) return PyErr_SetString(PyExc_TypeError, "'analyze' requires 1st parameter as callable"), nullptr;
				if (!PyCallable_Check(receiver)) return PyErr_SetString(PyExc_TypeError, "'analyze' requires 2nd parameter as callable"), nullptr;
				self->inst->analyze(max(topN, (size_t)10), [&reader](size_t id)->u16string
				{
					UniquePyObj argList = Py_BuildValue("(n)", id);
					UniquePyObj retVal = PyEval_CallObject(reader, argList);
					if (!retVal) throw bad_exception();
					if (PyObject_Not(retVal))
					{
						return {};
					}
					if (!PyUnicode_Check(retVal)) throw runtime_error{ "reader must return a value in 'str' type" };
					auto utf8 = PyUnicode_AsUTF8(retVal);
					if (!utf8) throw bad_exception();
					return Kiwi::toU16(utf8);
				}, [&receiver, topN](size_t id, vector<KResult>&& res)
				{
					if (res.size() > topN) res.erase(res.begin() + topN, res.end());
					UniquePyObj argList = Py_BuildValue("(nN)", id, resToPyList(res));
					UniquePyObj ret = PyEval_CallObject(receiver, argList);
					if(!ret) throw bad_exception();
				}, matchOptions);
				Py_INCREF(Py_None);
				return Py_None;
			}
			catch (const bad_exception&)
			{
				return nullptr;
			}
			catch (const exception& e)
			{
				PyErr_SetString(PyExc_Exception, e.what());
				return nullptr;
			}
		}
	}
	return nullptr;
}


static PyObject* kiwi__perform(KiwiObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topN = 1, matchOptions = PatternMatcher::all;
	PyObject* reader, *receiver;
	size_t minCnt = 10, maxWordLen = 10;
	float minScore = 0.25f, posScore = -3;
	static const char* kwlist[] = { "reader", "receiver", "top_n", "match_options", "min_cnt", "max_word_len", "min_score", "pos_score", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|nnnnff", (char**)kwlist, 
		&reader, &receiver, &topN, &matchOptions, &minCnt, &maxWordLen, &minScore, &posScore)) return nullptr;
	try
	{
		if (!PyCallable_Check(reader)) return PyErr_SetString(PyExc_TypeError, "perform requires 1st parameter which is callable"), nullptr;
		if (!PyCallable_Check(receiver)) return PyErr_SetString(PyExc_TypeError, "perform requires 2nd parameter which is callable"), nullptr;

		self->inst->perform(max(topN, (size_t)10), [&reader](size_t id)->u16string
		{
			UniquePyObj argList = Py_BuildValue("(n)", id);
			UniquePyObj retVal = PyEval_CallObject(reader, argList);
			if (!retVal) throw bad_exception();
			if (PyObject_Not(retVal))
			{
				return {};
			}
			auto utf8 = PyUnicode_AsUTF8(retVal);
			if (!utf8) throw bad_exception();
			return Kiwi::toU16(utf8);
		}, [&receiver, topN](size_t id, vector<KResult>&& res)
		{
			if (res.size() > topN) res.erase(res.begin() + topN, res.end());
			UniquePyObj argList = Py_BuildValue("(nN)", id, resToPyList(res));
			UniquePyObj ret = PyEval_CallObject(receiver, argList);
			if (!ret) throw bad_exception();
		}, matchOptions, minCnt, maxWordLen, minScore, posScore);
		Py_INCREF(Py_None);
		return Py_None;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
	return nullptr;
}

static PyObject* kiwi__version(KiwiObject* self, void* closure)
{
	try
	{
		return Py_BuildValue("n", self->inst->getVersion());
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

PyObject* moduleInit()
{
	static PyModuleDef mod =
	{
		PyModuleDef_HEAD_INIT,
		"_kiwipiepy",
		"Kiwi API for Python",
		-1,
		nullptr
	};

	gModule = PyModule_Create(&mod);

	if (PyType_Ready(&Kiwi_type) < 0) return nullptr;
	Py_INCREF(&Kiwi_type);
	PyModule_AddObject(gModule, "Kiwi", (PyObject*)&Kiwi_type);

	if (PyType_Ready(&KiwiAwaitableRes_type) < 0) return nullptr;
	Py_INCREF(&KiwiAwaitableRes_type);
	PyModule_AddObject(gModule, "_awaitable_res", (PyObject*)&KiwiAwaitableRes_type);

	if (PyType_Ready(&KiwiResIter_type) < 0) return nullptr;
	Py_INCREF(&KiwiResIter_type);
	PyModule_AddObject(gModule, "_res_iter", (PyObject*)&KiwiResIter_type);

	return gModule;
}

PyMODINIT_FUNC PyInit__kiwipiepy()
{
	return moduleInit();
}
