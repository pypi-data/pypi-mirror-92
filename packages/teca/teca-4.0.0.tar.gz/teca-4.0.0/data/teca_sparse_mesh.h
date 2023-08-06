#ifndef teca_sparse_mesh_h
#define teca_sparse_mesh_h

#include "teca_shared_object.h"
#include "teca_dataset.h"
#include "teca_metadata.h"
#include "teca_array_collection.h"

TECA_SHARED_OBJECT_FORWARD_DECL(teca_sparse_mesh)

/// class for geometric data
class teca_sparse_mesh : public teca_dataset
{
public:
    ~teca_sparse_mesh() = default;

    p_teca_array_collection get_point_arrays()
    { return m_impl->point_arrays; }

    const_p_teca_array_collection get_point_arrays() const
    { return m_impl->point_arrays; }

    // return true if the dataset is empty.
    bool empty() const noexcept override;

    // copy data and metadata. shallow copy uses reference
    // counting, while copy duplicates the data.
    void copy(const const_p_teca_dataset &) override;
    void shallow_copy(const p_teca_dataset &) override;

    // swap internals of the two objects
    void swap(p_teca_dataset &) override;

    // serialize the dataset to/from the given stream
    // for I/O or communication
    void to_stream(teca_binary_stream &) const override;
    void from_stream(teca_binary_stream &) override;

    // stream to/from human readable representation
    void to_stream(std::ostream &) const override;
    void from_stream(std::istream &) override {}

protected:
    teca_sparse_mesh();

public:
    struct impl_t
    {
        impl_t();
        //
        p_teca_array_collection arrays;
    };
    std::shared_ptr<impl_t> m_impl;
};

#endif
